import subprocess
import threading
import time
import platform
import requests
from config import LLAMAFILE_HOST, MODELS_DIR, get_active_model, get_llamafile_exe

_WINDOWS = platform.system() == "Windows"

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
            "--server",
            "-m", str(model),
            "--port", "8080",
            "--host", "127.0.0.1",
            "-ngl", "0",
            "-c", "2048",
        ]

        kwargs = dict(stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if _WINDOWS:
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        _process = subprocess.Popen(cmd, **kwargs)

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


def _wait_until_ready(timeout: int = 90) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        # If the process has already exited, grab its output and raise immediately
        if _process is not None and _process.poll() is not None:
            output = ""
            if _process.stdout:
                output = _process.stdout.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"llamafile exited unexpectedly (code {_process.returncode}).\n\n"
                f"Output:\n{output or '(none)'}\n\n"
                "On Windows, try right-clicking llamafile.exe, Properties > Unblock, then restart."
            )
        if is_ready():
            return
        time.sleep(1)
    raise TimeoutError("llamafile server did not respond within 90 seconds.")
