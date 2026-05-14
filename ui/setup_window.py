import threading
import customtkinter as ctk
from model_manager import download_default


class SetupWindow:
    """Shown on first launch when no model is present. Blocks until download completes."""

    def __init__(self, on_complete: callable, on_error: callable):
        self._on_complete = on_complete
        self._on_error = on_error

    def show(self) -> None:
        self._win = ctk.CTk()
        self._win.title("Student AI Support — First Time Setup")
        self._win.geometry("480x260")
        self._win.resizable(False, False)
        self._win.protocol("WM_DELETE_WINDOW", self._on_cancel)

        ctk.CTkLabel(
            self._win,
            text="Welcome to Student AI Support",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(28, 6))

        ctk.CTkLabel(
            self._win,
            text="We need to download the AI model on first run.\nThis is a one-time download (~1.9 GB) and requires an internet connection.",
            justify="center",
        ).pack(pady=(0, 16))

        self._status_label = ctk.CTkLabel(self._win, text="Starting download...")
        self._status_label.pack()

        self._progress = ctk.CTkProgressBar(self._win, width=380)
        self._progress.set(0)
        self._progress.pack(pady=(8, 4))

        self._size_label = ctk.CTkLabel(self._win, text="", text_color="gray")
        self._size_label.pack()

        threading.Thread(target=self._download, daemon=True).start()
        self._win.mainloop()

    def _download(self) -> None:
        try:
            download_default(progress_callback=self._on_progress)
            self._win.after(0, self._finish)
        except Exception as e:
            self._win.after(0, lambda: self._fail(e))

    def _on_progress(self, downloaded: int, total: int) -> None:
        if total > 0:
            pct = downloaded / total
            mb_done = downloaded / 1_000_000
            mb_total = total / 1_000_000
            self._win.after(0, lambda: self._update_ui(pct, mb_done, mb_total))

    def _update_ui(self, pct: float, mb_done: float, mb_total: float) -> None:
        self._progress.set(pct)
        self._status_label.configure(text=f"Downloading... {pct:.0%}")
        self._size_label.configure(text=f"{mb_done:.0f} MB / {mb_total:.0f} MB")

    def _finish(self) -> None:
        self._status_label.configure(text="Download complete!")
        self._progress.set(1)
        self._win.after(800, lambda: (self._win.destroy(), self._on_complete()))

    def _fail(self, error: Exception) -> None:
        self._win.destroy()
        self._on_error(error)

    def _on_cancel(self) -> None:
        import sys
        sys.exit(0)
