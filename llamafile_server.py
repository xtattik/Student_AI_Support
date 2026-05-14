import subprocess
import threading
import time
import requests
from pathlib import Path
from config import LLAMAFILE_HOST, MODELS_DIR, get_active_model, get_llamafile_exe

_process: subprocess.Popen | None = None
_lock = threading.Lock()


def start(model_filename: str | None = None) -> None:
    global _process
    with _lock:
        if _process is not None:
            return

        exe = get_llamafile_exe()
        model = MODELS_DIR / (model_filename or get_active_model())

        if not model.exists():
            raise FileNotFoundError(f"Model not found: {model}")

        cmd = [
            str(exe),
            "--model", str(model),
            "--port", "8080",
            "--host", "127.0.0.1",
            "--nobrowser",
            "-ngl", "0",        # CPU only — no GPU assumption
            "--ctx-size", "2048",
        ]

        _process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
        )

    _wait_until_ready()


def stop() -> None:
    global _process
    with _lock:
        if _process is not None:
            _process.terminate()
            try:
                _process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                _process.kill()
            _process = None


def restart(model_filename: str | None = None) -> None:
    stop()
    start(model_filename)


def is_ready() -> bool:
    try:
        r = requests.get(f"{LLAMAFILE_HOST}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def _wait_until_ready(timeout: int = 60) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_ready():
            return
        time.sleep(1)
    raise TimeoutError("llamafile server did not start within 60 seconds.")
