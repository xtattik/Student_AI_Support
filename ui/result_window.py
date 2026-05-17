import threading
import customtkinter as ctk
from typing import Generator
from theme import TEAL, TEAL_HOVER, SKY_BLUE, CHARCOAL, WHITE, set_window_icon

ACTION_LABELS = {
    "explain":   "Explanation",
    "summarise": "Summary",
    "test_me":   "Test Questions",
}


class ResultWindow:
    def __init__(self, action: str, text_generator: Generator[str, None, None],
                 source_text: str = "", simplify_prompt: str = ""):
        self._action = action
        self._generator = text_generator
        self._source_text = source_text
        self._simplify_prompt = simplify_prompt
        self._win: ctk.CTkToplevel | None = None
        self._simplify_btn = None

    def show(self) -> None:
        self._win = ctk.CTkToplevel()
        self._win.title(ACTION_LABELS.get(self._action, "Result"))
        self._win.geometry("620x460")
        self._win.attributes("-topmost", True)
        self._win.resizable(True, True)
        self._win.after(200, lambda: set_window_icon(self._win))

        # Coloured header strip
        header = ctk.CTkFrame(self._win, fg_color=TEAL, height=44, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text=ACTION_LABELS.get(self._action, "Result"),
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=WHITE,
        ).pack(side="left", padx=16, pady=10)

        self._textbox = ctk.CTkTextbox(self._win, wrap="word", font=ctk.CTkFont(size=13))
        self._textbox.pack(fill="both", expand=True, padx=16, pady=(12, 8))
        self._textbox.configure(state="disabled")

        # Button row
        btn_frame = ctk.CTkFrame(self._win, fg_color="transparent")
        btn_frame.pack(pady=(0, 16))

        ctk.CTkButton(
            btn_frame,
            text="Close",
            fg_color=TEAL,
            hover_color=TEAL_HOVER,
            text_color=WHITE,
            command=self._win.destroy,
        ).pack(side="left", padx=8)

        # "Simpler please" only appears on explanations
        if self._action == "explain" and self._simplify_prompt:
            self._simplify_btn = ctk.CTkButton(
                btn_frame,
                text="Simpler please",
                fg_color=SKY_BLUE,
                hover_color=TEAL,
                text_color=WHITE,
                command=self._simplify,
            )
            self._simplify_btn.pack(side="left", padx=8)

        threading.Thread(target=self._stream_text, daemon=True).start()

    def _simplify(self) -> None:
        self._simplify_btn.configure(state="disabled", text="Simplifying…")
        self._textbox.configure(state="normal")
        self._textbox.delete("1.0", "end")
        self._textbox.configure(state="disabled")
        import llm_engine
        self._generator = llm_engine.complete(self._simplify_prompt, self._source_text)
        threading.Thread(target=self._stream_text, daemon=True).start()

    def _stream_text(self) -> None:
        self._textbox.configure(state="normal")
        try:
            for chunk in self._generator:
                self._textbox.insert("end", chunk)
                self._textbox.see("end")
                self._textbox.update_idletasks()
        except Exception as e:
            self._textbox.insert("end", f"\n\n[Error: {e}]")
        finally:
            self._textbox.configure(state="disabled")
            if self._simplify_btn:
                try:
                    self._simplify_btn.configure(state="normal", text="Simpler please")
                except Exception:
                    pass
