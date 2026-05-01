# © 2025 The Christman AI Project. All rights reserved.
#
# This code is released as part of a trauma-informed, dignity-first AI ecosystem
# designed to protect, empower, and elevate vulnerable populations.
#
# By using, modifying, or distributing this software, you agree to uphold the following:
# 1. Truth — No deception, no manipulation.
# 2. Dignity — Respect the autonomy and humanity of all users.
# 3. Protection — Never use this to exploit or harm vulnerable individuals.
# 4. Transparency — Disclose all modifications and contributions clearly.
# 5. No Erasure — Preserve the mission and ethical origin of this work.
#
# This is not just code. This is redemption in code.
# Contact: lumacognify@thechristmanaiproject.com
# https://thechristmanaiproject.com

#!/usr/bin/env python3
"""
QUICK FIX for Learning Hub on Mac
Run this after pulling from GitHub to ensure Learning Hub works.
"""

import os
import subprocess
import sys

print("=" * 80)
print("ALPHAVOX LEARNING HUB - QUICK FIX")
print("=" * 80)
print()

# Check if we're in a virtual environment
in_venv = hasattr(sys, "real_prefix") or (
    hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
)

if not in_venv:
    print("⚠️  WARNING: Virtual environment not detected!")
    print("   Please activate your venv first:")
    print("   source venv/bin/activate")
    print()
    response = input("Continue anyway? (y/n): ")
    if response.lower() != "y":
        sys.exit(1)

print("Step 1: Installing/updating required packages...")
print("-" * 80)

try:
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("✅ Packages installed successfully")
except subprocess.CalledProcessError as e:
    print(f"❌ Error installing packages: {e}")
    sys.exit(1)

print()
print("Step 2: Verifying Learning Hub components...")
print("-" * 80)

# Test imports
try:
    print("Testing Flask import...", end=" ")
    import flask

    print(f"✅ Flask {flask.__version__}")
except ImportError as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

try:
    print("Testing learning_journey import...", end=" ")
    from learning_journey import LearningJourney

    print("✅ Success")
except ImportError as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

try:
    print("Testing learning_routes import...", end=" ")
    from learning_routes import learning_bp

    print("✅ Success")
except ImportError as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# Check data files
print()
print("Checking data files...", end=" ")
data_files = [
    "data/knowledge/topics.json",
    "data/knowledge/facts.json",
    "templates/learning/hub.html",
]

all_exist = all(os.path.exists(f) for f in data_files)
if all_exist:
    print("✅ All data files present")
else:
    print("⚠️  Some data files missing")
    for f in data_files:
        status = "✅" if os.path.exists(f) else "❌"
        print(f"  {status} {f}")

print()
print("=" * 80)
print("LEARNING HUB READY!")
print("=" * 80)
print()
print("Start AlphaVox with:")
print("  python app.py --port 5001")
print()
print("Then visit:")
print("  http://localhost:5001/learning")
print()
print("Features available:")
print("  • Browse Topics (/learning/topics)")
print("  • View Facts (/learning/facts)")
print("  • Learning Journey (/learning/journey)")
print("  • Knowledge Graph (/learning/graph)")
print()
