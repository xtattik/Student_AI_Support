import json
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

MODELS_DIR  = BASE_DIR / "models"
BIN_DIR     = BUNDLE_DIR / "bin"
ASSETS_DIR  = BUNDLE_DIR / "assets"
CONFIG_FILE = BASE_DIR / "config.json"

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

HOTKEY = "<ctrl>+<shift>+a"

_EXE_NAME = "llamafile.exe" if platform.system() == "Windows" else "llamafile"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"active_model": DEFAULT_MODEL_FILE}


def save_config(data: dict) -> None:
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_active_model() -> str:
    return load_config().get("active_model", DEFAULT_MODEL_FILE)


def set_active_model(filename: str) -> None:
    cfg = load_config()
    cfg["active_model"] = filename
    save_config(cfg)


def is_junior_mode() -> bool:
    return load_config().get("junior_mode", False)


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
