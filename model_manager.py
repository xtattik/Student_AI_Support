import shutil
from pathlib import Path
from typing import Callable
import requests
from huggingface_hub import hf_hub_url
from config import BASE_DIR, MODELS_DIR, get_models_dir, DEFAULT_MODEL_FILE, DEFAULT_MODEL_REPO, AVAILABLE_MODELS


def migrate_models_if_needed() -> int:
    """Silently move .gguf files from the legacy folder (next to the exe) to
    the current models dir (AppData/ApplicationSupport).  Returns files moved."""
    legacy = BASE_DIR / "models"
    dest_dir = get_models_dir()
    if legacy.resolve() == dest_dir.resolve():
        return 0  # same location — nothing to do (dev mode)
    if not legacy.exists():
        return 0
    files = list(legacy.glob("*.gguf"))
    if not files:
        return 0
    moved = 0
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            dest = dest_dir / f.name
            if not dest.exists():
                shutil.move(str(f), str(dest))
                moved += 1
    except Exception:
        pass  # best-effort — old path still works as fallback
    return moved


def has_any_model() -> bool:
    d = get_models_dir()
    return d.exists() and any(d.glob("*.gguf"))


def get_default_model_path() -> Path | None:
    p = get_models_dir() / DEFAULT_MODEL_FILE
    return p if p.exists() else None


def list_local_models() -> list[Path]:
    d = get_models_dir()
    if not d.exists():
        return []
    return sorted(d.glob("*.gguf"))


def models_dir_size_gb() -> float:
    """Return total size of all .gguf files in the models directory, in GB."""
    total = sum(f.stat().st_size for f in list_local_models())
    return total / 1_073_741_824


def download_model(
    repo_id: str,
    filename: str,
    progress_callback: Callable[[int, int], None] | None = None,
) -> Path:
    d = get_models_dir()
    d.mkdir(parents=True, exist_ok=True)

    dest = d / filename
    if dest.exists():
        return dest

    url = hf_hub_url(repo_id=repo_id, filename=filename)

    tmp = dest.with_suffix(".part")
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 256):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total:
                        progress_callback(downloaded, total)
        tmp.rename(dest)
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise

    return dest


def download_default(progress_callback: Callable[[int, int], None] | None = None) -> Path:
    return download_model(DEFAULT_MODEL_REPO, DEFAULT_MODEL_FILE, progress_callback)


def get_model_info(filename: str) -> dict | None:
    for m in AVAILABLE_MODELS:
        if m["filename"] == filename:
            return m
    return None
