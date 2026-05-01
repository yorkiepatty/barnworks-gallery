import re

_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b\d{2}/\d{2}/\d{4}\b"),
    re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    re.compile(r"\bMRN[:\s]*\w+\b", re.I),
]


def redact(text: str) -> str:
    if not text:
        return text
    t = text
    for pat in _PATTERNS:
        t = pat.sub("[REDACTED]", t)
    return (t[:256] + "…") if len(t) > 256 else t

__all__ = ['redact']
