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
Diagnostic script to identify why Learning Hub isn't loading on Mac.
This will trace every step of the import and registration process.
"""

import os
import sys
import traceback
from pathlib import Path

print("=" * 80)
print("LEARNING HUB DIAGNOSTIC SCRIPT")
print("=" * 80)
print()

# Check Python version
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print()

# Check current working directory
print(f"Current Directory: {os.getcwd()}")
print(f"Script Directory: {Path(__file__).parent}")
print()

# Check if key files exist
print("FILE EXISTENCE CHECK:")
print("-" * 80)
files_to_check = [
    "learning_journey.py",
    "learning_routes.py",
    "routes/learning_routes.py",
    "learning_analytics.py",
    "knowledge_engine.py",
    "learning_service.py",
    "templates/learning/hub.html",
    "templates/learning/topics.html",
]

for file_path in files_to_check:
    exists = "✅" if os.path.exists(file_path) else "❌"
    size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    print(f"{exists} {file_path:<40} ({size:,} bytes)")
print()

# Test imports one by one
print("IMPORT TESTING:")
print("-" * 80)


def test_import(module_name, description):
    """Test importing a single module and report results."""
    try:
        print(f"Testing: {description}")
        print(f"  Module: {module_name}")

        if "." in module_name:
            # Handle submodule imports
            parts = module_name.split(".")
            mod = __import__(module_name)
            for part in parts[1:]:
                mod = getattr(mod, part)
        else:
            mod = __import__(module_name)

        print("  ✅ SUCCESS")

        # Show what's in the module
        if hasattr(mod, "__file__"):
            print(f"  Location: {mod.__file__}")

        # Show key attributes
        attrs = [a for a in dir(mod) if not a.startswith("_")]
        if attrs:
            print(f"  Exports: {', '.join(attrs[:10])}")
            if len(attrs) > 10:
                print(f"           ... and {len(attrs) - 10} more")

        print()
        return True

    except Exception as e:
        print(f"  ❌ FAILED: {type(e).__name__}: {str(e)}")
        print("  Traceback:")
        for line in traceback.format_exc().split("\n"):
            if line.strip():
                print(f"    {line}")
        print()
        return False


# Test core dependencies first
print("\n1. CORE DEPENDENCIES:")
test_import("flask", "Flask framework")
test_import("flask.Blueprint", "Flask blueprints")

print("\n2. LEARNING SYSTEM CORE:")
learning_journey_ok = test_import("learning_journey", "Learning journey module")

print("\n3. LEARNING DEPENDENCIES:")
test_import("learning_analytics", "Learning analytics")
test_import("knowledge_engine", "Knowledge engine")
test_import("learning_service", "Learning service")

print("\n4. LEARNING ROUTES:")
routes_ok = test_import("learning_routes", "Main learning routes")
routes_dir_ok = test_import("routes.learning_routes", "Routes directory version")

# Test blueprint registration
print("\n5. BLUEPRINT REGISTRATION TEST:")
print("-" * 80)
if learning_journey_ok and routes_ok:
    try:
        from flask import Flask

        from learning_routes import learning_bp

        print("Creating test Flask app...")
        test_app = Flask(__name__)
        test_app.config["SECRET_KEY"] = "test"

        print(f"Blueprint name: {learning_bp.name}")
        print(f"Blueprint url_prefix: {learning_bp.url_prefix}")

        print("Attempting to register blueprint...")
        test_app.register_blueprint(learning_bp)

        print("✅ Blueprint registered successfully!")
        print("\nRegistered routes:")
        for rule in test_app.url_map.iter_rules():
            if "learning" in rule.rule:
                print(f"  {rule.methods} {rule.rule} -> {rule.endpoint}")

    except Exception as e:
        print(f"❌ Blueprint registration failed: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
else:
    print("⚠️  Cannot test blueprint registration - dependencies failed")

# Check for common issues
print("\n6. COMMON ISSUES CHECK:")
print("-" * 80)

# Check for circular imports
print("Checking for circular import issues...")
try:
    import importlib

    import learning_journey

    importlib.reload(learning_journey)
    print("✅ No circular import detected in learning_journey")
except Exception as e:
    print(f"❌ Possible circular import: {e}")

# Check Flask version
try:
    import flask

    print(f"Flask version: {flask.__version__}")
    if flask.__version__ < "2.0":
        print("⚠️  Warning: Old Flask version detected")
except Exception:
    safe_warn("operation_failed")
    raise
# Check if templates directory is accessible
from pathlib import Path

templates_dir = Path(__file__).parent / "templates" / "learning"
if templates_dir.exists():
    template_files = list(templates_dir.glob("*.html"))
    print(f"✅ Templates directory accessible ({len(template_files)} files)")
else:
    print("❌ Templates directory not found")

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
print()
print("RECOMMENDATIONS:")
print("-" * 80)

if not learning_journey_ok:
    print("❌ CRITICAL: learning_journey.py failed to import")
    print("   → This is the root cause of your 404 error")
    print("   → Check the error message above for missing dependencies")
    print("   → Run: pip install -r requirements.txt")
    print()

if learning_journey_ok and not (routes_ok or routes_dir_ok):
    print("❌ CRITICAL: learning_routes.py failed to import")
    print("   → Routes exist but can't be loaded")
    print("   → Check for syntax errors in learning_routes.py")
    print()

if learning_journey_ok and (routes_ok or routes_dir_ok):
    print("✅ All imports successful!")
    print("   → Learning Hub should be working")
    print("   → If still getting 404, check app.py route registration")
    print("   → Run app with: python app.py --port 5001")
    print("   → Check console output for route registration messages")
    print()

print("Next steps:")
print("1. Run this script on your Mac: python diagnose_learning_hub_mac.py")
print("2. Share the output with me")
print("3. I'll identify exactly what's different between Mac and codespace")
print()

__all__ = ['test_import']
