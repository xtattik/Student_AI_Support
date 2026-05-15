import time
import pyperclip
from pynput.keyboard import Key, Controller

_keyboard = Controller()


def get_selected_text() -> tuple[str, bool]:
    """
    Try to capture highlighted text via Ctrl+C.
    Falls back to whatever is already on the clipboard (for PDFs/Adobe Reader
    where focus loss deselects text before Ctrl+C can fire).

    Returns (text, used_fallback) so the caller can hint the user if needed.
    """
    pre_existing = _safe_get_clipboard()

    # Clear clipboard so we can detect whether Ctrl+C actually captured anything
    pyperclip.copy("")
    time.sleep(0.05)

    _keyboard.press(Key.ctrl)
    _keyboard.press("c")
    _keyboard.release("c")
    _keyboard.release(Key.ctrl)

    time.sleep(0.2)

    captured = pyperclip.paste().strip()

    if captured:
        # Ctrl+C worked — restore original and return captured text
        if pre_existing:
            pyperclip.copy(pre_existing)
        return captured, False

    # Ctrl+C got nothing — fall back to whatever was already on clipboard
    if pre_existing and pre_existing.strip():
        return pre_existing.strip(), True

    return "", False
