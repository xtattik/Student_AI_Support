"""
Run this once to download the llamafile server binary into bin/.
Usage: python download_llamafile.py
"""
import sys
import urllib.request
from pathlib import Path

VERSION = "0.10.1"
URL = f"https://github.com/mozilla-ai/llamafile/releases/download/{VERSION}/llamafile-{VERSION}-thin"
DEST = Path(__file__).parent / "bin" / "llamafile.exe"


def main():
    DEST.parent.mkdir(exist_ok=True)
    if DEST.exists():
        print(f"llamafile.exe already present at {DEST}")
        return

    print(f"Downloading llamafile v{VERSION} (~43 MB)...")

    def _progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            pct = min(downloaded / total_size * 100, 100)
            print(f"\r  {pct:.1f}%", end="", flush=True)

    urllib.request.urlretrieve(URL, DEST, reporthook=_progress)
    print(f"\nSaved to {DEST}")


if __name__ == "__main__":
    main()
