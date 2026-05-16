import threading
import customtkinter as ctk
from model_manager import list_local_models, download_model
from config import (AVAILABLE_MODELS, get_active_model, is_junior_mode, set_junior_mode,
                    get_hotkey, set_hotkey, get_hotkey_display)
from theme import TEAL, TEAL_HOVER, LIME_GREEN, CHARCOAL, WHITE
import llm_engine


class SettingsWindow:
    def __init__(self):
        self._win: ctk.CTkToplevel | None = None

    def show(self) -> None:
        if self._win is not None:
            self._win.focus_force()
            return

        self._win = ctk.CTkToplevel()
        self._win.title("Settings — Student AI Support")
        self._win.geometry("500x580")
        self._win.resizable(False, True)
        self._win.protocol("WM_DELETE_WINDOW", self._close)

        header = ctk.CTkFrame(self._win, fg_color=TEAL, height=44, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Settings",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=WHITE,
        ).pack(side="left", padx=16, pady=10)

        ctk.CTkLabel(
            self._win,
            text="Active Model",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEAL,
        ).pack(padx=20, pady=(16, 4), anchor="w")

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
            fg_color=TEAL,
            button_color=TEAL_HOVER,
            button_hover_color=TEAL_HOVER,
            text_color=WHITE,
        )
        dropdown.pack(padx=20, pady=(8, 16), anchor="w")

        # ── Mode toggle ──────────────────────────────────────────────
        ctk.CTkLabel(
            self._win,
            text="Language Mode",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEAL,
        ).pack(padx=20, pady=(4, 2), anchor="w")

        mode_frame = ctk.CTkFrame(self._win, fg_color="transparent")
        mode_frame.pack(fill="x", padx=20, pady=(0, 12))

        self._junior_var = ctk.BooleanVar(value=is_junior_mode())
        ctk.CTkSwitch(
            mode_frame,
            text="Junior mode  (simpler language, ages 9–10)",
            variable=self._junior_var,
            onvalue=True,
            offvalue=False,
            fg_color=TEAL,
            progress_color=TEAL,
            command=lambda: set_junior_mode(self._junior_var.get()),
        ).pack(side="left", padx=10, pady=4)

        # ── Hotkey ───────────────────────────────────────────────────
        ctk.CTkLabel(
            self._win,
            text="Launch Hotkey",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEAL,
        ).pack(padx=20, pady=(4, 2), anchor="w")

        ctk.CTkLabel(
            self._win,
            text="Tick modifiers, type a single key, then press Apply.",
            text_color="gray",
        ).pack(padx=20, anchor="w")

        hk_frame = ctk.CTkFrame(self._win, fg_color="transparent")
        hk_frame.pack(fill="x", padx=20, pady=(6, 12))

        h = get_hotkey()
        self._hk_ctrl  = ctk.BooleanVar(value=h.get("ctrl",  True))
        self._hk_shift = ctk.BooleanVar(value=h.get("shift", True))
        self._hk_alt   = ctk.BooleanVar(value=h.get("alt",   False))

        ctk.CTkCheckBox(hk_frame, text="Ctrl",  variable=self._hk_ctrl,
                        fg_color=TEAL, hover_color=TEAL_HOVER, checkmark_color=WHITE,
                        ).pack(side="left", padx=(0, 8))
        ctk.CTkCheckBox(hk_frame, text="Shift", variable=self._hk_shift,
                        fg_color=TEAL, hover_color=TEAL_HOVER, checkmark_color=WHITE,
                        ).pack(side="left", padx=(0, 8))
        ctk.CTkCheckBox(hk_frame, text="Alt",   variable=self._hk_alt,
                        fg_color=TEAL, hover_color=TEAL_HOVER, checkmark_color=WHITE,
                        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(hk_frame, text="+", text_color=CHARCOAL).pack(side="left", padx=(0, 6))

        self._hk_key_entry = ctk.CTkEntry(hk_frame, width=44, justify="center")
        self._hk_key_entry.insert(0, h.get("key", "`"))
        self._hk_key_entry.pack(side="left", padx=(0, 12))

        self._hk_status = ctk.CTkLabel(hk_frame, text="", text_color="gray")
        self._hk_status.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            hk_frame,
            text="Apply",
            width=72,
            fg_color=TEAL,
            hover_color=TEAL_HOVER,
            text_color=WHITE,
            command=self._apply_hotkey,
        ).pack(side="right")

        # ── Download models ──────────────────────────────────────────
        ctk.CTkLabel(
            self._win,
            text="Download Models",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEAL,
        ).pack(padx=20, pady=(0, 6), anchor="w")

        for m in AVAILABLE_MODELS:
            self._model_row(m)

        ctk.CTkButton(
            self._win,
            text="Close",
            fg_color=TEAL,
            hover_color=TEAL_HOVER,
            text_color=WHITE,
            command=self._close,
        ).pack(pady=16)

    def _model_row(self, model_info: dict) -> None:
        frame = ctk.CTkFrame(self._win, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=3)

        from config import MODELS_DIR
        dest = MODELS_DIR / model_info["filename"]

        # Pack right-side widgets first so they claim space before the label expands
        status_label = ctk.CTkLabel(frame, text="", width=80, text_color="gray")
        status_label.pack(side="right", padx=(0, 6))

        if dest.exists():
            status_label.configure(text="Downloaded", text_color=LIME_GREEN)
        else:
            btn = ctk.CTkButton(
                frame,
                text="Download",
                width=90,
                fg_color=TEAL,
                hover_color=TEAL_HOVER,
                text_color=WHITE,
                command=lambda m=model_info, lbl=status_label: self._start_download(m, lbl),
            )
            btn.pack(side="right", padx=(0, 6), pady=4)

        label_text = model_info["label"]
        if model_info["note"]:
            label_text += f"  ({model_info['note']})"
        ctk.CTkLabel(frame, text=label_text, anchor="w", text_color=CHARCOAL).pack(
            side="left", padx=10, pady=6, expand=True, fill="x"
        )

    def _start_download(self, model_info: dict, status_label: ctk.CTkLabel) -> None:
        status_label.configure(text="Downloading...", text_color="gray")

        def _run():
            try:
                download_model(model_info["repo"], model_info["filename"])
                status_label.configure(text="Downloaded", text_color=LIME_GREEN)
            except Exception:
                status_label.configure(text="Failed", text_color="red")

        threading.Thread(target=_run, daemon=True).start()

    def _apply_hotkey(self) -> None:
        import hotkey_listener
        key = self._hk_key_entry.get().strip()
        if len(key) != 1:
            self._hk_status.configure(text="Type exactly 1 key", text_color="red")
            return
        if not (self._hk_ctrl.get() or self._hk_shift.get() or self._hk_alt.get()):
            self._hk_status.configure(text="Pick at least one modifier", text_color="red")
            return
        h = {
            "ctrl":  self._hk_ctrl.get(),
            "shift": self._hk_shift.get(),
            "alt":   self._hk_alt.get(),
            "key":   key,
        }
        set_hotkey(h)
        hotkey_listener.restart()
        self._hk_status.configure(
            text=f"Active: {get_hotkey_display(h)}", text_color=LIME_GREEN
        )

    def _on_model_select(self, value: str) -> None:
        llm_engine.switch_model(value)

    def _close(self) -> None:
        if self._win:
            self._win.destroy()
            self._win = None
