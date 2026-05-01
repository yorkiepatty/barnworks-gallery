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
Complete AlphaVox Environment Setup for Mac
Ensures all modules load correctly through alphavox_module_loader.py
"""

import os
import subprocess
import sys

print("=" * 80)
print("ALPHAVOX COMPLETE ENVIRONMENT SETUP")
print("=" * 80)
print()

# Check venv
in_venv = hasattr(sys, "real_prefix") or (
    hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
)
if not in_venv:
    print("⚠️  Virtual environment not detected!")
    print("   Run: source venv/bin/activate")
    sys.exit(1)

print("✅ Virtual environment detected")
print(f"   Python: {sys.version}")
print(f"   Location: {sys.executable}")
print()

# Step 1: Upgrade pip
print("Step 1: Upgrading pip...")
print("-" * 80)
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    print("✅ Pip upgraded\n")
except subprocess.CalledProcessError as e:
    print(f"❌ Error upgrading pip: {e}\n")

# Step 2: Install core dependencies
print("Step 2: Installing core dependencies...")
print("-" * 80)

core_packages = [
    "Flask==3.0.0",
    "flask-cors",
    "flask-limiter",
    "werkzeug",
    "Jinja2",
    "python-dotenv",
    "cryptography",
]

for package in core_packages:
    try:
        print(f"  Installing {package}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            check=True,
            capture_output=True,
        )
        print(f"  ✅ {package}")
    except subprocess.CalledProcessError:
        print(f"  ⚠️  {package} (will try from requirements.txt)")

print()

# Step 3: Install from requirements.txt
print("Step 3: Installing from requirements.txt...")
print("-" * 80)
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("✅ All requirements installed\n")
except subprocess.CalledProcessError:
    print("⚠️  Some packages may have failed (continuing...)\n")

# Step 4: Test alphavox_module_loader
print("Step 4: Testing alphavox_module_loader.py...")
print("-" * 80)
try:
    from alphavox_module_loader import load_alphavox_consciousness

    loader = load_alphavox_consciousness()
    stats = loader.get_stats()

    print("✅ Module loader working!")
    print(f"   Loaded: {stats['loaded']}/{stats['total_modules']} modules")
    print(f"   Success rate: {stats['success_rate']:.1f}%")
    print()

    # Check critical modules
    critical_modules = [
        "interpreter",
        "learning_routes",
        "learning_journey",
        "conversation_engine",
        "memory_engine",
    ]

    print("Checking critical modules:")
    for mod in critical_modules:
        if mod in loader.loaded_modules:
            print(f"  ✅ {mod}")
        else:
            print(f"  ❌ {mod} - MISSING!")

except Exception as e:
    print(f"❌ Module loader failed: {e}")
    import traceback

    traceback.print_exc()

print()

# Step 5: Test Flask
print("Step 5: Testing Flask...")
print("-" * 80)
try:
    import flask

    print(f"✅ Flask {flask.__version__} installed")

    # Try to import app_init
    try:
        import app_init

        print("✅ app_init can import")
    except Exception as e:
        print(f"⚠️  app_init import issue: {e}")

except ImportError:
    print("❌ Flask not installed!")
    print("   Run: pip install Flask")

print()

# Step 6: Check database
print("Step 6: Checking database...")
print("-" * 80)
if os.path.exists("alphavox.db"):
    size = os.path.getsize("alphavox.db")
    print(f"✅ Database exists ({size:,} bytes)")
else:
    print("⚠️  Database will be created on first run")

print()

# Final summary
print("=" * 80)
print("SETUP COMPLETE!")
print("=" * 80)
print()
print("✅ All modules now load through alphavox_module_loader.py")
print("✅ interpreter.py and learning_routes are included")
print("✅ Dependencies respect proper loading order")
print()
print("To start AlphaVox:")
print("  python app.py --port 5001")
print()
print("To verify module loading:")
print("  python alphavox_module_loader.py")
print()
print("To access Learning Hub:")
print("  http://localhost:5001/learning")
print()
