import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
BIN_DIR = BASE_DIR / "bin"
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


def get_llamafile_exe() -> Path:
    exe = BIN_DIR / "llamafile.exe"
    if not exe.exists():
        raise FileNotFoundError(
            f"llamafile.exe not found at {exe}\n"
            "Download it from https://github.com/Mozilla-Ocho/llamafile/releases "
            "and place it in the bin/ folder."
        )
    return exe
