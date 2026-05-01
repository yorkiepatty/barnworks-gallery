import os, re, sys
ROOT = os.path.abspath(os.path.dirname(__file__))

allowed_dotdirs = {".github"}
critical = {
    "brain.py",
    "alphavox_ultimate_voice.py",
    "conversation_loop.py",
    "tts_bridge.py",
    "nlp_integration.py",
    "alphavox_input_nlu.py",
    "memory_engine.py",
    "memory_engine_secure.py",
    "routes_module.py",
    "research_module.py",
    "security_config.py",
    "production_app.py",
    "main.py",
}

violations = []

def is_hidden_path(path):
    parts = os.path.normpath(path).split(os.sep)
    return any(p.startswith(".") for p in parts if p not in (".", ".."))

for dirpath, dirnames, filenames in os.walk(ROOT):
    if dirpath.endswith(os.sep + "venv") or os.sep + ".venv" in dirpath:
        dirnames[:] = []
        continue

    # block hidden dirs except .github
    parts = os.path.relpath(dirpath, ROOT).split(os.sep)
    for p in parts:
        if p.startswith(".") and p not in allowed_dotdirs and p not in (".", ""):
            violations.append(f"hidden-dir: {dirpath}")
            break

    for fn in filenames:
        rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)

        if rel.startswith("venv/") or rel.startswith(".venv/"):
            continue

        if fn.endswith(".pyi"):
            violations.append(f"pyi-forbidden: {rel}")

        if fn == "logging.py" and "site-packages" not in dirpath:
            violations.append(f"stdlib-shadow: {rel}")

        if "/logging/__init__.py" in rel.replace("\\","/"):
            violations.append(f"stdlib-shadow: {rel}")

        if rel.replace("\\","/").count("/") >= 1 and fn in critical:
            violations.append(f"critical-not-root: {rel}")

        if rel.endswith(".py"):
            try:
                with open(os.path.join(dirpath, fn), "r", encoding="utf-8", errors="ignore") as f:
                    s = f.read()
            except Exception:
                continue

            if re.search(r"\bsys\.path\.(append|insert)\s*\(", s):
                violations.append(f"sys-path-hack: {rel}")

            if re.search(r"\bfrom\s+app\.sec\s+import\s+logging\b", s) or re.search(r"\bapp\.sec\.logging\b", s):
                violations.append(f"logging-shadow-import: {rel}")

            if re.search(r"^\s*import\s+logging\s+as\s+", s, re.M):
                violations.append(f"logging-alias: {rel}")

# Only .github is allowed as a dotdir at top level
top = set(name for name in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, name)) and name.startswith("."))
for d in top:
    if d not in allowed_dotdirs:
        violations.append(f"top-dotdir: {d}")

if violations:
    print("repo-guard violations")
    for v in sorted(set(violations)):
        print(v)
    sys.exit(1)

print("repo-guard OK")


__all__ = ['is_hidden_path']
