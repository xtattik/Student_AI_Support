import requests
from typing import Generator
from config import LLAMAFILE_HOST


def complete(system_prompt: str, user_text: str, stream: bool = True) -> Generator[str, None, None]:
    payload = {
        "model": "local",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
        "stream": stream,
    }

    with requests.post(
        f"{LLAMAFILE_HOST}/v1/chat/completions",
        json=payload,
        stream=stream,
        timeout=120,
    ) as response:
        response.raise_for_status()

        if not stream:
            data = response.json()
            yield data["choices"][0]["message"]["content"]
            return

        for line in response.iter_lines():
            if not line:
                continue
            text = line.decode("utf-8")
            if text.startswith("data: "):
                text = text[6:]
            if text == "[DONE]":
                break
            try:
                import json
                chunk = json.loads(text)
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    yield delta
            except Exception:
                continue
