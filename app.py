import sys
import customtkinter as ctk
import llm_engine
import hotkey_listener
from clipboard_handler import get_selected_text
from overlay import OverlayWindow
from ui.result_window import ResultWindow
from ui.test_window import TestWindow
from ui.setup_window import SetupWindow
from ui.settings_window import SettingsWindow
from system_tray import TrayIcon
from model_manager import has_any_model
import prompts

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

_settings_window = SettingsWindow()


def _get_prompt(action: str) -> str:
    return {
        "explain": prompts.EXPLAIN,
        "summarise": prompts.SUMMARISE,
        "test_me": prompts.TEST_ME,
    }[action]


def _on_action(action: str) -> None:
    text = get_selected_text()
    if not text:
        _show_error("No text selected", "Please highlight some text before using the hotkey.")
        return

    system_prompt = _get_prompt(action)
    generator = llm_engine.complete(system_prompt, text)

    def _open():
        if action == "test_me":
            win = TestWindow(source_text=text, generator=generator)
        else:
            win = ResultWindow(action, generator)
        win.show()

    _root.after(0, _open)


def _on_hotkey() -> None:
    _root.after(0, _overlay.show)


def _show_error(title: str, message: str) -> None:
    def _open():
        win = ctk.CTkToplevel(_root)
        win.title(title)
        win.geometry("360x140")
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text=message, wraplength=320, justify="center").pack(expand=True)
        ctk.CTkButton(win, text="OK", command=win.destroy).pack(pady=(0, 16))
    _root.after(0, _open)


def _launch_app() -> None:
    global _root, _overlay

    _root = ctk.CTk()
    _root.withdraw()

    _overlay = OverlayWindow(on_action=_on_action)

    tray = TrayIcon(
        on_settings=lambda: _root.after(0, _settings_window.show),
        on_quit=_quit,
    )
    tray.start()

    hotkey_listener.start(_on_hotkey)

    # Pre-load the model in the background so first response is faster
    llm_engine.preload()

    _root.mainloop()


def _quit() -> None:
    hotkey_listener.stop()
    _root.after(0, _root.quit)


def main() -> None:
    if not has_any_model():
        setup = SetupWindow(
            on_complete=_launch_app,
            on_error=lambda e: (print(f"Download failed: {e}"), sys.exit(1)),
        )
        setup.show()
    else:
        _launch_app()


if __name__ == "__main__":
    main()
