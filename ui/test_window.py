import re
import threading
import customtkinter as ctk
from typing import Generator
from theme import TEAL, TEAL_HOVER, LIME_GREEN, CHARCOAL, WHITE


def parse_questions(text: str) -> list[dict]:
    questions = []
    blocks = re.split(r'\n(?=\d+\.)', text.strip())
    for block in blocks:
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        q_match = re.match(r'^\d+\.\s*(.+)', lines[0])
        if not q_match:
            continue
        question_text = q_match.group(1)
        options = {}
        for line in lines[1:]:
            opt_match = re.match(r'^([A-D])\)\s*(.+)', line)
            if opt_match:
                options[opt_match.group(1)] = opt_match.group(2)
        if len(options) == 4:
            questions.append({"question": question_text, "options": options})
    return questions


class TestWindow:
    def __init__(self, source_text: str, generator: Generator[str, None, None]):
        self._source_text = source_text
        self._generator = generator
        self._win: ctk.CTkToplevel | None = None
        self._answer_vars: list[ctk.StringVar] = []

    def show(self) -> None:
        self._win = ctk.CTkToplevel()
        self._win.title("Test Yourself")
        self._win.geometry("640x200")
        self._win.attributes("-topmost", True)
        self._win.resizable(True, True)

        header = ctk.CTkFrame(self._win, fg_color=TEAL, height=44, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Test Yourself",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=WHITE,
        ).pack(side="left", padx=16, pady=10)

        self._loading = ctk.CTkLabel(
            self._win,
            text="Generating questions...",
            font=ctk.CTkFont(size=14),
            text_color=CHARCOAL,
        )
        self._loading.pack(expand=True)

        threading.Thread(target=self._collect_and_render, daemon=True).start()

    def _collect_and_render(self) -> None:
        try:
            full_text = "".join(self._generator)
            questions = parse_questions(full_text)
            if questions:
                self._win.after(0, lambda: self._render_questions(questions))
            else:
                self._win.after(0, lambda: self._show_raw(full_text))
        except Exception as e:
            self._win.after(0, lambda: self._show_raw(f"[Error: {e}]"))

    def _render_questions(self, questions: list[dict]) -> None:
        self._loading.destroy()
        self._win.geometry("680x540")
        self._answer_vars = []

        scroll = ctk.CTkScrollableFrame(self._win)
        scroll.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        for i, q in enumerate(questions):
            ctk.CTkLabel(
                scroll,
                text=f"Q{i + 1}. {q['question']}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=TEAL,
                wraplength=600,
                justify="left",
                anchor="w",
            ).pack(anchor="w", pady=(10, 4))

            var = ctk.StringVar(value="")
            self._answer_vars.append(var)

            for letter, text in q["options"].items():
                ctk.CTkRadioButton(
                    scroll,
                    text=f"{letter})  {text}",
                    variable=var,
                    value=letter,
                    font=ctk.CTkFont(size=12),
                    fg_color=TEAL,
                    hover_color=TEAL_HOVER,
                ).pack(anchor="w", padx=20, pady=2)

        self._questions = questions

        self._check_btn = ctk.CTkButton(
            self._win,
            text="Check my answers",
            fg_color=TEAL,
            hover_color=TEAL_HOVER,
            text_color=WHITE,
            command=self._check_answers,
        )
        self._check_btn.pack(pady=12)

    def _check_answers(self) -> None:
        answers = [v.get() for v in self._answer_vars]
        if any(a == "" for a in answers):
            self._show_status("Please answer all questions before checking.", "orange")
            return

        self._check_btn.configure(state="disabled", text="Checking...")

        qa_lines = []
        for i, (q, ans) in enumerate(zip(self._questions, answers)):
            option_text = q["options"].get(ans, ans)
            qa_lines.append(f"Q{i+1}: {q['question']}\nStudent answered: {ans}) {option_text}")

        qa_summary = "\n\n".join(qa_lines)
        threading.Thread(target=self._run_check, args=(qa_summary,), daemon=True).start()

    def _run_check(self, qa_summary: str) -> None:
        from llm_client import complete
        from prompts import CHECK_ANSWERS

        prompt = CHECK_ANSWERS.format(
            source_text=self._source_text[:2000],
            qa_summary=qa_summary,
        )
        try:
            result = "".join(complete(system_prompt="You are a helpful tutor.", user_text=prompt))
            self._win.after(0, lambda: self._show_feedback(result))
        except Exception as e:
            self._win.after(0, lambda: self._show_status(f"Error: {e}", "red"))

    def _show_feedback(self, text: str) -> None:
        self._check_btn.pack_forget()

        # Colour each result line based on correct/incorrect keywords
        feedback_box = ctk.CTkTextbox(self._win, wrap="word", font=ctk.CTkFont(size=13), height=180)
        feedback_box.pack(fill="x", padx=16, pady=(0, 4))
        feedback_box.insert("end", text)
        feedback_box.configure(state="disabled")

        ctk.CTkButton(
            self._win,
            text="Close",
            fg_color=TEAL,
            hover_color=TEAL_HOVER,
            text_color=WHITE,
            command=self._win.destroy,
        ).pack(pady=(0, 12))

    def _show_raw(self, text: str) -> None:
        self._loading.destroy()
        self._win.geometry("640x440")
        box = ctk.CTkTextbox(self._win, wrap="word", font=ctk.CTkFont(size=13))
        box.pack(fill="both", expand=True, padx=16, pady=16)
        box.insert("end", text)
        box.configure(state="disabled")
        ctk.CTkButton(
            self._win,
            text="Close",
            fg_color=TEAL,
            hover_color=TEAL_HOVER,
            text_color=WHITE,
            command=self._win.destroy,
        ).pack(pady=(0, 12))

    def _show_status(self, msg: str, colour: str = "gray") -> None:
        if hasattr(self, "_status_label"):
            self._status_label.configure(text=msg, text_color=colour)
        else:
            self._status_label = ctk.CTkLabel(self._win, text=msg, text_color=colour)
            self._status_label.pack()
