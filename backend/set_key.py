# set_key.py
import os, re, sys, base64, argparse, textwrap
from pathlib import Path

def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def is_fernet_key(s: str) -> bool:
    try:
        raw = base64.urlsafe_b64decode(s.encode())
        return len(raw) == 32 and all(c in b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" for c in s.encode().rstrip(b"="))
    except Exception:
        return False

def gen_fernet_key() -> str:
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        die("cryptography not installed. pip install cryptography")
    return Fernet.generate_key().decode()

ARN_RE = re.compile(r"^arn:aws:kms:[a-z0-9-]+:\d{12}:(key/[0-9a-f-]{36}|alias/[A-Za-z0-9/_+=,.@-]+)$")
ALIAS_RE = re.compile(r"^alias/[A-Za-z0-9/_+=,.@-]+$")

def looks_like_kms(s: str) -> bool:
    return bool(ARN_RE.match(s) or ALIAS_RE.match(s))

def write_env(env_path: Path, updates: dict):
    # read existing (if any)
    lines = []
    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    # map existing keys
    existing = {}
    for i, line in enumerate(lines):
        if not line or line.strip().startswith("#") or "=" not in line:
            continue
        k = line.split("=", 1)[0].strip()
        existing[k] = i

    # apply updates
    for k, v in updates.items():
        v = v.strip()
        if "=" in v and v.startswith(k + "="):
            # user accidentally pasted NAME=value as value
            v = v.split("=", 1)[1]
        nv = f"{k}={v}"
        if k in existing:
            lines[existing[k]] = nv
        else:
            lines.append(nv)

    # ensure utf-8 no-bom
    content = "\n".join(lines).strip() + "\n"
    env_path.write_text(content, encoding="utf-8")

def set_keyring(name: str, value: str):
    try:
        import keyring
    except ImportError:
        die("keyring not installed. pip install keyring (or use --no-keyring)")
    keyring.set_password("alphavox", name, value)

def kms_describe(ident: str, region: str | None):
    try:
        import boto3
    except ImportError:
        print("boto3 not installed; skipping KMS check.")
        return None
    kms = boto3.client("kms", region_name=region)
    meta = kms.describe_key(KeyId=ident)["KeyMetadata"]
    return meta  # dict

def main():
    p = argparse.ArgumentParser(
        description="Set and validate AlphaVox keys (.env + optional keyring).",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument("--fernet", help="Fernet key (urlsafe base64, 32 bytes).")
    p.add_argument("--gen", action="store_true", help="Generate a new Fernet key.")
    p.add_argument("--kms", help="KMS key ARN or alias/NAME.")
    p.add_argument("--region", default=os.getenv("AWS_REGION") or "us-east-1", help="AWS region for KMS check.")
    p.add_argument("--env-file", default=".env", help="Path to .env")
    p.add_argument("--no-keyring", action="store_true", help="Do not write to OS keyring.")
    p.add_argument("--check", action="store_true", help="Only validate and print; do not write.")
    args = p.parse_args()

    updates = {}

    # Fernet
    fernet_val = args.fernet
    if args.gen:
        fernet_val = gen_fernet_key()
        print(f"[ok] generated Fernet key: {fernet_val}")

    if fernet_val:
        if fernet_val.startswith("ALPHAVOX_ENCRYPTION_KEY="):
            fernet_val = fernet_val.split("=", 1)[1]
        if not is_fernet_key(fernet_val):
            die("ALPHAVOX_ENCRYPTION_KEY is not a valid Fernet key (must decode to 32 bytes, urlsafe base64)")
        updates["ALPHAVOX_ENCRYPTION_KEY"] = fernet_val
        print("[ok] Fernet key validated")

    # KMS
    if args.kms:
        kms_val = args.kms.strip()
        if kms_val.startswith("ALPHAVOX_KMS_KEY_ID=") or kms_val.startswith("KMS_KEY_ID="):
            kms_val = kms_val.split("=", 1)[1]
        if not looks_like_kms(kms_val):
            die("KMS identifier must be a full ARN or alias/NAME")
        updates["ALPHAVOX_KMS_KEY_ID"] = kms_val
        print("[ok] KMS key format looks valid")
        # try to resolve to ARN if creds exist
        try:
            meta = kms_describe(kms_val, args.region)
            if meta:
                print(f"[ok] KMS reachable: {meta['Arn']}")
        except Exception as e:
            print(f"[warn] KMS describe failed: {e}")

    if args.check:
        print("[check] no writes performed")
        return

    # Write .env
    env_path = Path(args.env_file)
    write_env(env_path, updates)
    print(f"[ok] wrote {env_path.resolve()}")

    # Write keyring unless disabled
    if not args.no_keyring:
        if "ALPHAVOX_ENCRYPTION_KEY" in updates:
            set_keyring("ALPHAVOX_ENCRYPTION_KEY", updates["ALPHAVOX_ENCRYPTION_KEY"])
            print("[ok] stored Fernet key in keyring (service=alphavox)")
        if "ALPHAVOX_KMS_KEY_ID" in updates:
            set_keyring("ALPHAVOX_KMS_KEY_ID", updates["ALPHAVOX_KMS_KEY_ID"])
            print("[ok] stored KMS id in keyring (service=alphavox)")

    print("[done] keys set. restart your app so it picks up .env or keyring.")

if __name__ == "__main__":
    main()
