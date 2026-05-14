import tkinter as tk
import customtkinter as ctk
from pynput.mouse import Controller as MouseController

_mouse = MouseController()

BUTTON_ACTIONS = [
    ("Explain this", "explain"),
    ("Summarise this", "summarise"),
    ("Test me on this", "test_me"),
]


class OverlayWindow:
    def __init__(self, on_action: callable):
        self._on_action = on_action
        self._win: ctk.CTk | None = None

    def show(self) -> None:
        if self._win is not None:
            self.hide()

        x, y = _mouse.position

        self._win = ctk.CTkToplevel()
        self._win.title("")
        self._win.overrideredirect(True)
        self._win.attributes("-topmost", True)
        self._win.resizable(False, False)

        frame = ctk.CTkFrame(self._win, corner_radius=10)
        frame.pack(padx=2, pady=2)

        label = ctk.CTkLabel(frame, text="What would you like?", font=ctk.CTkFont(size=13, weight="bold"))
        label.pack(padx=16, pady=(12, 6))

        for text, action in BUTTON_ACTIONS:
            btn = ctk.CTkButton(
                frame,
                text=text,
                width=200,
                command=lambda a=action: self._handle(a),
            )
            btn.pack(padx=16, pady=4)

        cancel = ctk.CTkButton(
            frame,
            text="Cancel",
            width=200,
            fg_color="transparent",
            border_width=1,
            command=self.hide,
        )
        cancel.pack(padx=16, pady=(4, 12))

        self._win.update_idletasks()
        w = self._win.winfo_width()
        h = self._win.winfo_height()

        screen_w = self._win.winfo_screenwidth()
        screen_h = self._win.winfo_screenheight()
        px = min(x + 10, screen_w - w - 10)
        py = min(y + 10, screen_h - h - 10)

        self._win.geometry(f"+{px}+{py}")
        self._win.focus_force()
        self._win.bind("<FocusOut>", lambda _: self.hide())
        self._win.bind("<Escape>", lambda _: self.hide())

    def hide(self) -> None:
        if self._win is not None:
            self._win.destroy()
            self._win = None

    def _handle(self, action: str) -> None:
        self.hide()
        self._on_action(action)
