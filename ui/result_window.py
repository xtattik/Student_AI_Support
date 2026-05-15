import threading
import customtkinter as ctk
from typing import Generator
from theme import TEAL, TEAL_HOVER, CHARCOAL, WHITE, set_window_icon

ACTION_LABELS = {
    "explain": "Explanation",
    "summarise": "Summary",
    "test_me": "Test Questions",
}

ACTION_COLOURS = {
    "explain":   TEAL,
    "summarise": TEAL,
    "test_me":   TEAL,
}


class ResultWindow:
    def __init__(self, action: str, text_generator: Generator[str, None, None]):
        self._action = action
        self._generator = text_generator
        self._win: ctk.CTkToplevel | None = None

    def show(self) -> None:
        self._win = ctk.CTkToplevel()
        self._win.title(ACTION_LABELS.get(self._action, "Result"))
        self._win.geometry("620x460")
        self._win.attributes("-topmost", True)
        self._win.resizable(True, True)
        set_window_icon(self._win)

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

        ctk.CTkButton(
            self._win,
            text="Close",
            fg_color=TEAL,
            hover_color=TEAL_HOVER,
            text_color=WHITE,
            command=self._win.destroy,
        ).pack(pady=(0, 16))

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
