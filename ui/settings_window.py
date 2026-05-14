import threading
import customtkinter as ctk
from model_manager import list_local_models, download_model, get_model_info
from config import AVAILABLE_MODELS, get_active_model, set_active_model
import llamafile_server


class SettingsWindow:
    def __init__(self):
        self._win: ctk.CTkToplevel | None = None

    def show(self) -> None:
        if self._win is not None:
            self._win.focus_force()
            return

        self._win = ctk.CTkToplevel()
        self._win.title("Settings — Student AI Support")
        self._win.geometry("500x400")
        self._win.resizable(False, False)
        self._win.protocol("WM_DELETE_WINDOW", self._close)

        ctk.CTkLabel(
            self._win,
            text="AI Model",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(padx=20, pady=(20, 6), anchor="w")

        ctk.CTkLabel(
            self._win,
            text="Select a model or download additional ones below.",
            text_color="gray",
        ).pack(padx=20, anchor="w")

        local = [p.name for p in list_local_models()]
        active = get_active_model()

        self._model_var = ctk.StringVar(value=active if active in local else (local[0] if local else ""))
        dropdown = ctk.CTkOptionMenu(
            self._win,
            values=local or ["No models downloaded"],
            variable=self._model_var,
            command=self._on_model_select,
        )
        dropdown.pack(padx=20, pady=(8, 16), anchor="w")

        ctk.CTkLabel(
            self._win,
            text="Download models",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(padx=20, pady=(0, 6), anchor="w")

        for m in AVAILABLE_MODELS:
            self._model_row(m)

        ctk.CTkButton(self._win, text="Close", command=self._close).pack(pady=20)

    def _model_row(self, model_info: dict) -> None:
        frame = ctk.CTkFrame(self._win)
        frame.pack(fill="x", padx=20, pady=3)

        label_text = model_info["label"]
        if model_info["note"]:
            label_text += f"  ({model_info['note']})"
        ctk.CTkLabel(frame, text=label_text, anchor="w").pack(side="left", padx=10, pady=6, expand=True, fill="x")

        status_label = ctk.CTkLabel(frame, text="", width=80, text_color="gray")
        status_label.pack(side="right", padx=(0, 6))

        from config import MODELS_DIR
        dest = MODELS_DIR / model_info["filename"]
        if dest.exists():
            status_label.configure(text="Downloaded")
        else:
            btn = ctk.CTkButton(
                frame,
                text="Download",
                width=90,
                command=lambda m=model_info, lbl=status_label: self._start_download(m, lbl),
            )
            btn.pack(side="right", padx=(0, 6), pady=4)

    def _start_download(self, model_info: dict, status_label: ctk.CTkLabel) -> None:
        status_label.configure(text="Downloading...")

        def _run():
            try:
                download_model(model_info["repo"], model_info["filename"])
                status_label.configure(text="Downloaded")
            except Exception as e:
                status_label.configure(text="Failed")

        threading.Thread(target=_run, daemon=True).start()

    def _on_model_select(self, value: str) -> None:
        set_active_model(value)
        threading.Thread(target=llamafile_server.restart, kwargs={"model_filename": value}, daemon=True).start()

    def _close(self) -> None:
        if self._win:
            self._win.destroy()
            self._win = None
