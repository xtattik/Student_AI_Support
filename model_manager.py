from pathlib import Path
from typing import Callable
from huggingface_hub import hf_hub_download
from config import MODELS_DIR, DEFAULT_MODEL_FILE, DEFAULT_MODEL_REPO, AVAILABLE_MODELS


def has_any_model() -> bool:
    return any(MODELS_DIR.glob("*.gguf"))


def get_default_model_path() -> Path | None:
    p = MODELS_DIR / DEFAULT_MODEL_FILE
    return p if p.exists() else None


def list_local_models() -> list[Path]:
    return sorted(MODELS_DIR.glob("*.gguf"))


def download_model(
    repo_id: str,
    filename: str,
    progress_callback: Callable[[int, int], None] | None = None,
) -> Path:
    MODELS_DIR.mkdir(exist_ok=True)

    dest = MODELS_DIR / filename
    if dest.exists():
        return dest

    class _ProgressHandler:
        def __init__(self, cb):
            self.cb = cb
            self._downloaded = 0

        def __call__(self, downloaded: int, total: int):
            if self.cb:
                self.cb(downloaded, total)

    handler = _ProgressHandler(progress_callback) if progress_callback else None

    path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=str(MODELS_DIR),
        local_dir_use_symlinks=False,
    )

    return Path(path)


def download_default(progress_callback: Callable[[int, int], None] | None = None) -> Path:
    return download_model(DEFAULT_MODEL_REPO, DEFAULT_MODEL_FILE, progress_callback)


def get_model_info(filename: str) -> dict | None:
    for m in AVAILABLE_MODELS:
        if m["filename"] == filename:
            return m
    return None
