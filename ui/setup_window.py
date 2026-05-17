import threading
import tkinter.filedialog as fd
import customtkinter as ctk
from pathlib import Path
from model_manager import download_default, has_any_model
from config import get_models_dir, set_models_dir, DEFAULT_MODEL_FILE
from theme import TEAL, TEAL_HOVER, CHARCOAL, WHITE, SKY_BLUE, load_logo, set_window_icon


class SetupWindow:
    """Shown on first launch when no model is present.
    Lets the user confirm (or change) the models folder, detects existing models,
    then downloads if needed. Calls on_complete when ready to launch."""

    def __init__(self, on_complete: callable, on_error: callable):
        self._on_complete = on_complete
        self._on_error = on_error
        self._done = False
        self._error = None

    def show(self) -> None:
        self._win = ctk.CTk()
        self._win.title("Student AI Support — First Time Setup")
        self._win.geometry("500x360")
        self._win.resizable(False, False)
        self._win.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self._win.after(200, lambda: set_window_icon(self._win))

        # ── Header ────────────────────────────────────────────────────
        header = ctk.CTkFrame(self._win, fg_color=TEAL, height=56, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        try:
            logo_img = load_logo((40, 40))
            ctk.CTkLabel(header, image=logo_img, text="").pack(side="left", padx=(12, 8), pady=8)
        except Exception:
            pass
        ctk.CTkLabel(
            header, text="Marsden Park Anglican College",
            font=ctk.CTkFont(size=13, weight="bold"), text_color=WHITE,
        ).pack(side="left", pady=8)

        # ── Title ─────────────────────────────────────────────────────
        ctk.CTkLabel(
            self._win, text="First Time Setup",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=CHARCOAL,
        ).pack(pady=(18, 4))

        ctk.CTkLabel(
            self._win,
            text="The AI model (~1.9 GB) needs to be downloaded once.\n"
                 "If you already have the model file, just point to that folder.",
            justify="center", text_color=CHARCOAL,
        ).pack(pady=(0, 12))

        # ── Folder picker row ─────────────────────────────────────────
        ctk.CTkLabel(
            self._win, text="Models folder:",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=TEAL,
        ).pack(padx=20, anchor="w")

        path_frame = ctk.CTkFrame(self._win, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=(2, 12))

        self._path_var = ctk.StringVar(value=str(get_models_dir()))
        path_entry = ctk.CTkEntry(
            path_frame, textvariable=self._path_var,
            state="readonly", font=ctk.CTkFont(size=11),
        )
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            path_frame, text="Change…", width=80,
            fg_color=SKY_BLUE, hover_color=TEAL, text_color=WHITE,
            command=self._pick_folder,
        ).pack(side="left")

        # ── Status + progress ─────────────────────────────────────────
        self._status_label = ctk.CTkLabel(
            self._win, text="", text_color=CHARCOAL,
        )
        self._status_label.pack(pady=(0, 4))

        self._progress = ctk.CTkProgressBar(self._win, width=420, progress_color=TEAL)
        self._progress.set(0)
        self._progress.pack(pady=(0, 2))
        self._progress.pack_forget()  # hidden until download starts

        self._size_label = ctk.CTkLabel(self._win, text="", text_color="gray")
        self._size_label.pack()

        # ── Action button ─────────────────────────────────────────────
        self._action_btn = ctk.CTkButton(
            self._win, text="Start Download",
            fg_color=TEAL, hover_color=TEAL_HOVER, text_color=WHITE,
            width=160, command=self._start,
        )
        self._action_btn.pack(pady=(8, 0))

        # Check immediately whether the model already exists at the chosen path
        self._check_existing()

        self._win.mainloop()

        if self._error:
            self._on_error(self._error)
        elif self._done:
            self._on_complete()

    # ── Folder selection ───────────────────────────────────────────────────────

    def _pick_folder(self) -> None:
        chosen = fd.askdirectory(title="Choose models folder", mustexist=False)
        if not chosen:
            return
        p = Path(chosen)
        set_models_dir(p)
        self._path_var.set(str(p))
        self._check_existing()

    def _check_existing(self) -> None:
        """If the default model is already in the chosen folder, skip the download."""
        model_path = Path(self._path_var.get()) / DEFAULT_MODEL_FILE
        if model_path.exists():
            self._status_label.configure(
                text=f"✓ Model found in this folder — no download needed.",
                text_color=TEAL,
            )
            self._action_btn.configure(text="Continue  →", command=self._skip)
        else:
            self._status_label.configure(
                text="No model found here yet — ready to download.",
                text_color=CHARCOAL,
            )
            self._action_btn.configure(text="Start Download", command=self._start)

    # ── Download ───────────────────────────────────────────────────────────────

    def _start(self) -> None:
        self._action_btn.configure(state="disabled", text="Downloading…")
        self._progress.pack(pady=(0, 2))
        threading.Thread(target=self._download, daemon=True).start()

    def _download(self) -> None:
        try:
            download_default(progress_callback=self._on_progress)
            self._win.after(0, self._finish)
        except Exception as e:
            self._error = e
            self._win.after(0, self._win.destroy)

    def _on_progress(self, downloaded: int, total: int) -> None:
        if total > 0 and self._win_alive():
            pct    = downloaded / total
            mb_done  = downloaded / 1_000_000
            mb_total = total / 1_000_000
            self._win.after(0, lambda p=pct, d=mb_done, t=mb_total: self._update_ui(p, d, t))

    def _update_ui(self, pct: float, mb_done: float, mb_total: float) -> None:
        if not self._win_alive():
            return
        self._progress.set(pct)
        self._status_label.configure(text=f"Downloading… {pct:.0%}")
        self._size_label.configure(text=f"{mb_done:.0f} MB / {mb_total:.0f} MB")

    def _finish(self) -> None:
        if not self._win_alive():
            return
        self._done = True
        self._status_label.configure(text="Download complete!")
        self._progress.set(1)
        self._win.after(800, self._win.destroy)

    def _skip(self) -> None:
        self._done = True
        self._win.destroy()

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _win_alive(self) -> bool:
        try:
            return bool(self._win.winfo_exists())
        except Exception:
            return False

    def _on_cancel(self) -> None:
        import sys
        sys.exit(0)
