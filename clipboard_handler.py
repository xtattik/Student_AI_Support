import time
import pyperclip
from pynput.keyboard import Key, Controller

_keyboard = Controller()


def get_selected_text() -> str:
    original = _safe_get_clipboard()

    pyperclip.copy("")
    time.sleep(0.05)

    _keyboard.press(Key.ctrl)
    _keyboard.press("c")
    _keyboard.release("c")
    _keyboard.release(Key.ctrl)

    time.sleep(0.15)

    selected = pyperclip.paste().strip()

    if original:
        pyperclip.copy(original)

    return selected


def _safe_get_clipboard() -> str:
    try:
        return pyperclip.paste()
    except Exception:
        return ""
