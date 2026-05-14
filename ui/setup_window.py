import threading
import customtkinter as ctk
from model_manager import download_default
from theme import TEAL, TEAL_HOVER, CHARCOAL, WHITE, SKY_BLUE, load_logo


class SetupWindow:
    """Shown on first launch when no model is present. Blocks until download completes."""

    def __init__(self, on_complete: callable, on_error: callable):
        self._on_complete = on_complete
        self._on_error = on_error
        self._done = False
        self._error: Exception | None = None

    def show(self) -> None:
        self._win = ctk.CTk()
        self._win.title("Student AI Support — First Time Setup")
        self._win.geometry("480x300")
        self._win.resizable(False, False)
        self._win.protocol("WM_DELETE_WINDOW", self._on_cancel)

        # Header
        header = ctk.CTkFrame(self._win, fg_color=TEAL, height=56, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        try:
            logo_img = load_logo((40, 40))
            ctk.CTkLabel(header, image=logo_img, text="").pack(side="left", padx=(12, 8), pady=8)
        except Exception:
            pass

        ctk.CTkLabel(
            header,
            text="Marsden Park Anglican College",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=WHITE,
        ).pack(side="left", pady=8)

        ctk.CTkLabel(
            self._win,
            text="Student AI Support — First Time Setup",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=CHARCOAL,
        ).pack(pady=(20, 4))

        ctk.CTkLabel(
            self._win,
            text="We need to download the AI model on first run.\nThis is a one-time download (~1.9 GB) and requires an internet connection.",
            justify="center",
            text_color=CHARCOAL,
        ).pack(pady=(0, 14))

        self._status_label = ctk.CTkLabel(self._win, text="Starting download...", text_color=CHARCOAL)
        self._status_label.pack()

        self._progress = ctk.CTkProgressBar(self._win, width=380, progress_color=TEAL)
        self._progress.set(0)
        self._progress.pack(pady=(8, 4))

        self._size_label = ctk.CTkLabel(self._win, text="", text_color="gray")
        self._size_label.pack()

        threading.Thread(target=self._download, daemon=True).start()
        self._win.mainloop()

        if self._error:
            self._on_error(self._error)
        elif self._done:
            self._on_complete()

    def _download(self) -> None:
        try:
            download_default(progress_callback=self._on_progress)
            self._win.after(0, self._finish)
        except Exception as e:
            self._error = e
            self._win.after(0, self._win.destroy)

    def _on_progress(self, downloaded: int, total: int) -> None:
        if total > 0 and self._win_alive():
            pct = downloaded / total
            mb_done = downloaded / 1_000_000
            mb_total = total / 1_000_000
            self._win.after(0, lambda p=pct, d=mb_done, t=mb_total: self._update_ui(p, d, t))

    def _update_ui(self, pct: float, mb_done: float, mb_total: float) -> None:
        if not self._win_alive():
            return
        self._progress.set(pct)
        self._status_label.configure(text=f"Downloading... {pct:.0%}")
        self._size_label.configure(text=f"{mb_done:.0f} MB / {mb_total:.0f} MB")

    def _finish(self) -> None:
        if not self._win_alive():
            return
        self._done = True
        self._status_label.configure(text="Download complete!")
        self._progress.set(1)
        self._win.after(800, self._win.destroy)

    def _win_alive(self) -> bool:
        try:
            return bool(self._win.winfo_exists())
        except Exception:
            return False

    def _on_cancel(self) -> None:
        import sys
        sys.exit(0)
