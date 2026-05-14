import threading
from PIL import Image, ImageDraw
import pystray


def _make_icon() -> Image.Image:
    img = Image.new("RGB", (64, 64), color=(30, 100, 200))
    d = ImageDraw.Draw(img)
    d.text((18, 18), "AI", fill=(255, 255, 255))
    return img


class TrayIcon:
    def __init__(self, on_settings: callable, on_quit: callable):
        self._on_settings = on_settings
        self._on_quit = on_quit
        self._icon: pystray.Icon | None = None

    def start(self) -> None:
        menu = pystray.Menu(
            pystray.MenuItem("Settings", lambda: self._on_settings()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", lambda: self._quit()),
        )
        self._icon = pystray.Icon(
            "StudentAI",
            _make_icon(),
            "Student AI Support\nCtrl+Shift+A to use",
            menu,
        )
        threading.Thread(target=self._icon.run, daemon=True).start()

    def _quit(self) -> None:
        if self._icon:
            self._icon.stop()
        self._on_quit()

    def stop(self) -> None:
        if self._icon:
            self._icon.stop()
