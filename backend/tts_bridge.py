from typing import Optional
import pathlib
import shutil
import tempfile
from subprocess import run


def _resolve(cmd: str) -> str:
    p = shutil.which(cmd)
    if not p:
        raise FileNotFoundError(cmd)
    return p


def synth_to_file(text: str) -> str:
    nf = tempfile.NamedTemporaryFile(delete=False, suffix=".aiff")
    nf.close()
    run([_resolve("say"), text, "-o", nf.name], check=True, timeout=30)  # nosec B603
    return nf.name


def play_file(path: str) -> None:
    p = pathlib.Path(path)
    if p.suffix.lower() not in {".aiff", ".wav", ".mp3"}:
        raise ValueError("unsupported audio type")
    run([_resolve("afplay"), str(p)], check=True, timeout=30)  # nosec B603


def speak_response(text: str, voice: Optional[str] = None) -> None:
    return None

__all__ = ['_resolve', 'synth_to_file', 'play_file', 'speak_response']
