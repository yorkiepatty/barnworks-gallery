# secrets_env.py
import os, base64

def get_encryption_key():
    k = os.getenv("ALPHAVOX_ENCRYPTION_KEY") or os.getenv("ALPHAVOX_MASTER_KEY")
    if not k:
        raise RuntimeError("Missing ALPHAVOX_ENCRYPTION_KEY (or ALPHAVOX_MASTER_KEY)")
    try:
        raw = base64.urlsafe_b64decode((k + "==").encode())
    except Exception as e:
        raise RuntimeError(f"Bad Fernet key format: {e}")
    if len(raw) != 32:
        raise RuntimeError(f"Fernet key decodes to {len(raw)} bytes, expected 32.")
    return k


__all__ = ['get_encryption_key']
