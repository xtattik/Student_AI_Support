"""
Run once to download the llamafile server binary into bin/.
Works on Windows and macOS.
Usage: python download_llamafile.py
"""
import platform
import urllib.request
from pathlib import Path

VERSION  = "0.10.1"
BASE_URL = f"https://github.com/mozilla-ai/llamafile/releases/download/{VERSION}"

IS_WINDOWS = platform.system() == "Windows"
FILENAME   = "llamafile.exe" if IS_WINDOWS else "llamafile"
DEST       = Path(__file__).parent / "bin" / FILENAME


def main() -> None:
    DEST.parent.mkdir(exist_ok=True)

    if DEST.exists():
        print(f"llamafile binary already present at {DEST}")
        return

    url = f"{BASE_URL}/llamafile-{VERSION}-thin"
    print(f"Downloading llamafile v{VERSION} (~43 MB) from:\n  {url}")

    def _progress(block_num: int, block_size: int, total_size: int) -> None:
        downloaded = block_num * block_size
        if total_size > 0:
            pct = min(downloaded / total_size * 100, 100)
            print(f"\r  {pct:.1f}%", end="", flush=True)

    urllib.request.urlretrieve(url, DEST, reporthook=_progress)
    print(f"\nSaved to {DEST}")

    if not IS_WINDOWS:
        import stat
        DEST.chmod(DEST.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        print("Made executable (chmod +x)")


if __name__ == "__main__":
    main()
