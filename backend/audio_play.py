import pathlib
import subprocess


def safe_play(path: str):
    p = pathlib.Path(path)
    if p.suffix.lower() not in {".aiff", ".wav", ".mp3"}:
        raise ValueError("unsupported audio type")
    subprocess.run(["/usr/bin/afplay", str(p)], check=True, timeout=15)

__all__ = ['safe_play']
