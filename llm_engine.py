import threading
import platform
from typing import Generator
from config import get_models_dir, get_active_model, set_active_model

_llm = None
_current_model: str | None = None
_lock = threading.RLock()

# Apple Silicon: offload all layers to Metal GPU. Everywhere else: CPU only.
_GPU_LAYERS = -1 if (platform.system() == "Darwin" and platform.machine() == "arm64") else 0


def _do_load(model_filename: str) -> None:
    global _llm, _current_model
    from llama_cpp import Llama

    model_path = get_models_dir() / model_filename
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    if _llm is not None:
        _llm.close()
        _llm = None

    _llm = Llama(
        model_path=str(model_path),
        n_ctx=2048,
        n_gpu_layers=_GPU_LAYERS,
        verbose=False,
    )
    _current_model = model_filename


def preload(model_filename: str | None = None) -> None:
    """Load the model in a background thread on app startup."""
    target = model_filename or get_active_model()

    def _run():
        with _lock:
            if _llm is None or _current_model != target:
                _do_load(target)

    threading.Thread(target=_run, daemon=True).start()


def switch_model(model_filename: str) -> None:
    """Switch to a different model. Blocks until loaded."""
    def _run():
        with _lock:
            _do_load(model_filename)
        set_active_model(model_filename)

    threading.Thread(target=_run, daemon=True).start()


def is_ready() -> bool:
    return _llm is not None


def complete(system_prompt: str, user_text: str) -> Generator[str, None, None]:
    """Stream a completion. Blocks on first call until model is loaded."""
    with _lock:
        target = get_active_model()
        if _llm is None or _current_model != target:
            _do_load(target)

        stream = _llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            max_tokens=1024,
            temperature=0.3,
            stream=True,
        )

        for chunk in stream:
            delta = chunk["choices"][0]["delta"].get("content", "")
            if delta:
                yield delta
