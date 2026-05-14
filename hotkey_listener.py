import threading
from pynput import keyboard

_HOTKEY = "<ctrl>+<shift>+a"
_listener: keyboard.GlobalHotKeys | None = None


def start(callback: callable) -> None:
    global _listener

    def _on_trigger():
        threading.Thread(target=callback, daemon=True).start()

    _listener = keyboard.GlobalHotKeys({_HOTKEY: _on_trigger})
    _listener.start()


def stop() -> None:
    global _listener
    if _listener is not None:
        _listener.stop()
        _listener = None
