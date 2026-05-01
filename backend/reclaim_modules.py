import os
import shutil
from pathlib import Path

ROOT = Path("/Users/EverettN/ALPHAVOXWAKESUP")
BURIED_PATHS = ROOT.rglob("*.py")

TARGET_DIR = ROOT / "RECLAIMED_MODULES"
TARGET_DIR.mkdir(exist_ok=True)

IGNORED_DIRS = {".venv", "archive", "site-packages", "node_modules"}
LOGFILE = TARGET_DIR / "_reclaimed_log.txt"
IGNORED_LOG = TARGET_DIR / "_ignored_paths_log.txt"

reclaimed = []
ignored = []

for path in BURIED_PATHS:
    if any(ignored in str(path) for ignored in IGNORED_DIRS):
        ignored.append(str(path))
        continue

    try:
        dest = TARGET_DIR / path.name
        if not dest.exists():
            shutil.copy2(path, dest)
            reclaimed.append(f"✅ {path} → {dest.name}")
        else:
            reclaimed.append(f"⚠️ {path} skipped (duplicate name)")
    except Exception as e:
        reclaimed.append(f"❌ {path} failed: {str(e)}")

# Save logs
with open(LOGFILE, 'w') as log:
    log.write("\n".join(reclaimed))

with open(IGNORED_LOG, 'w') as log:
    log.write("\n".join(ignored))

    print("✅ Reclaim complete.")
    print(f"📦 Output: {TARGET_DIR.resolve()}")
    print(f"📜 Reclaimed: {RECLAIMED_LOG.resolve()}")
    print(f"❌ Skipped:   {SKIPPED_LOG.resolve()}")

