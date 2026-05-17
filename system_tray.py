import threading
import webbrowser
import pystray
from theme import load_logo_pil
from config import is_junior_mode, set_junior_mode

HELP_URL = "https://github.com/xtattik/Student_AI_Support#readme"


class TrayIcon:
    def __init__(self, on_settings: callable, on_quit: callable):
        self._on_settings = on_settings
        self._on_quit = on_quit
        self._icon: pystray.Icon | None = None

    def start(self) -> None:
        try:
            img = load_logo_pil((64, 64))
        except Exception:
            from PIL import Image, ImageDraw
            img = Image.new("RGB", (64, 64), color=(13, 107, 122))
            ImageDraw.Draw(img).text((18, 18), "AI", fill=(255, 255, 255))

        menu = pystray.Menu(
            pystray.MenuItem(
                "Junior mode",
                self._toggle_junior,
                checked=lambda _: is_junior_mode(),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Settings", lambda: self._on_settings()),
            pystray.MenuItem("Help", lambda: webbrowser.open(HELP_URL)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", lambda: self._quit()),
        )
        self._icon = pystray.Icon(
            "StudentAI",
            img,
            "Student AI Support\nHighlight text, then press Ctrl+Shift+`",
            menu,
        )
        threading.Thread(target=self._icon.run, daemon=True).start()

    def _toggle_junior(self) -> None:
        set_junior_mode(not is_junior_mode())

    def _quit(self) -> None:
        if self._icon:
            self._icon.stop()
        self._on_quit()

    def stop(self) -> None:
        if self._icon:
            self._icon.stop()
