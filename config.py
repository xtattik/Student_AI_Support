import json
import os
import sys
import platform
from pathlib import Path

# When frozen by PyInstaller, the exe lives in a known folder.
# User data (models, config.json) lives next to the exe.
# Bundled read-only assets (logo, bin/) are in sys._MEIPASS.
if getattr(sys, "frozen", False):
    BASE_DIR   = Path(sys.executable).parent   # writable — models, config.json
    BUNDLE_DIR = Path(sys._MEIPASS)            # read-only — assets, bin
else:
    BASE_DIR   = Path(__file__).parent
    BUNDLE_DIR = Path(__file__).parent

def _platform_models_dir() -> Path:
    """Return a models directory that won't be auto-synced by OneDrive or iCloud.
    Only redirects for frozen (packaged) builds — dev runs keep models next to the code."""
    if getattr(sys, "frozen", False):
        if platform.system() == "Windows":
            local = os.environ.get("LOCALAPPDATA")
            if local:
                return Path(local) / "StudentAI" / "models"
        elif platform.system() == "Darwin":
            return Path.home() / "Library" / "Application Support" / "StudentAI" / "models"
    return BASE_DIR / "models"

# Platform default — used as the fallback when no override is stored in config.json
MODELS_DIR = _platform_models_dir()

BIN_DIR     = BUNDLE_DIR / "bin"
ASSETS_DIR  = BUNDLE_DIR / "assets"
CONFIG_FILE = BASE_DIR / "config.json"

VERSION = "1.9.3"

LLAMAFILE_PORT = 8080
LLAMAFILE_HOST = f"http://127.0.0.1:{LLAMAFILE_PORT}"

DEFAULT_MODEL_REPO = "bartowski/Qwen2.5-3B-Instruct-GGUF"
DEFAULT_MODEL_FILE = "Qwen2.5-3B-Instruct-Q4_K_M.gguf"

AVAILABLE_MODELS = [
    {
        "label": "General (default)",
        "repo": "bartowski/Qwen2.5-3B-Instruct-GGUF",
        "filename": "Qwen2.5-3B-Instruct-Q4_K_M.gguf",
        "note": "",
    },
    {
        "label": "Coding & Tech",
        "repo": "bartowski/Qwen2.5-Coder-3B-Instruct-GGUF",
        "filename": "Qwen2.5-Coder-3B-Instruct-Q4_K_M.gguf",
        "note": "Best for CS / IT classes",
    },
    {
        "label": "Deeper explanations",
        "repo": "bartowski/Qwen2.5-7B-Instruct-GGUF",
        "filename": "Qwen2.5-7B-Instruct-Q4_K_M.gguf",
        "note": "Requires stronger laptop (8GB+ RAM)",
    },
]

# Default hotkey — Ctrl+Shift+` avoids browser conflicts (Ctrl+Shift+A opens tab managers)
_DEFAULT_HOTKEY = {"ctrl": True, "shift": True, "alt": False, "key": "`"}


def get_hotkey() -> dict:
    return load_config().get("hotkey", _DEFAULT_HOTKEY.copy())


def set_hotkey(h: dict) -> None:
    cfg = load_config()
    cfg["hotkey"] = h
    save_config(cfg)


def get_hotkey_pynput(h: dict | None = None) -> str:
    """Return the hotkey in pynput GlobalHotKeys format, e.g. '<ctrl>+<shift>+`'."""
    if h is None:
        h = get_hotkey()
    parts = []
    if h.get("ctrl",  False): parts.append("<ctrl>")
    if h.get("shift", False): parts.append("<shift>")
    if h.get("alt",   False): parts.append("<alt>")
    parts.append(h.get("key", "`"))
    return "+".join(parts)


def get_hotkey_display(h: dict | None = None) -> str:
    """Return a human-readable hotkey string, e.g. 'Ctrl + Shift + `'."""
    if h is None:
        h = get_hotkey()
    parts = []
    if h.get("ctrl",  False): parts.append("Ctrl")
    if h.get("shift", False): parts.append("Shift")
    if h.get("alt",   False): parts.append("Alt")
    key = h.get("key", "`")
    parts.append(key.upper() if len(key) == 1 else key)
    return " + ".join(parts)

_EXE_NAME = "llamafile.exe" if platform.system() == "Windows" else "llamafile"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"active_model": DEFAULT_MODEL_FILE}


def save_config(data: dict) -> None:
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_models_dir() -> Path:
    """Return the current models directory.
    Respects a user-set override in config.json; falls back to the platform default."""
    override = load_config().get("models_dir")
    if override:
        return Path(override)
    return MODELS_DIR  # platform default


def set_models_dir(path: Path | None) -> None:
    """Persist a custom models directory. Pass None to reset to the platform default."""
    cfg = load_config()
    if path is None:
        cfg.pop("models_dir", None)
    else:
        cfg["models_dir"] = str(path)
    save_config(cfg)


def get_active_model() -> str:
    return load_config().get("active_model", DEFAULT_MODEL_FILE)


def set_active_model(filename: str) -> None:
    cfg = load_config()
    cfg["active_model"] = filename
    save_config(cfg)


def is_junior_mode() -> bool:
    return load_config().get("junior_mode", False)


def is_first_run() -> bool:
    """True if the user hasn't been shown the welcome/setup wizard yet."""
    return not load_config().get("welcomed", False)


def mark_welcomed() -> None:
    cfg = load_config()
    cfg["welcomed"] = True
    save_config(cfg)


def set_junior_mode(value: bool) -> None:
    cfg = load_config()
    cfg["junior_mode"] = value
    save_config(cfg)


def get_llamafile_exe() -> Path:
    exe = BIN_DIR / _EXE_NAME
    if not exe.exists():
        raise FileNotFoundError(
            f"llamafile binary not found at {exe}\n"
            "Run download_llamafile.py to fetch it."
        )
    return exe
