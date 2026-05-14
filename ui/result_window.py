import threading
import customtkinter as ctk
from typing import Generator

ACTION_LABELS = {
    "explain": "Explanation",
    "summarise": "Summary",
    "test_me": "Test Questions",
}


class ResultWindow:
    def __init__(self, action: str, text_generator: Generator[str, None, None]):
        self._action = action
        self._generator = text_generator
        self._win: ctk.CTkToplevel | None = None

    def show(self) -> None:
        self._win = ctk.CTkToplevel()
        self._win.title(ACTION_LABELS.get(self._action, "Result"))
        self._win.geometry("600x450")
        self._win.attributes("-topmost", True)
        self._win.resizable(True, True)

        header = ctk.CTkLabel(
            self._win,
            text=ACTION_LABELS.get(self._action, "Result"),
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        header.pack(padx=16, pady=(16, 8), anchor="w")

        self._textbox = ctk.CTkTextbox(self._win, wrap="word", font=ctk.CTkFont(size=13))
        self._textbox.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        self._textbox.configure(state="disabled")

        close_btn = ctk.CTkButton(self._win, text="Close", command=self._win.destroy)
        close_btn.pack(pady=(0, 16))

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
