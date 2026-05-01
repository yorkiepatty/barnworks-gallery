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
Debug script to identify why AlphaVox won't stay running on Mac
"""

import os
import sys

print("=" * 80)
print("ALPHAVOX STARTUP DEBUG")
print("=" * 80)
print()

# Check if we're in the right directory
print("1. ENVIRONMENT CHECK:")
print("-" * 80)
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

# Check if key files exist
print("2. CHECKING CRITICAL FILES:")
print("-" * 80)
critical_files = [
    "app.py",
    "app_init.py",
    "db.py",
    "alphavox.db",
]

for file in critical_files:
    exists = "✅" if os.path.exists(file) else "❌"
    print(f"{exists} {file}")

print()

# Try to import Flask and check version
print("3. FLASK INSTALLATION:")
print("-" * 80)
try:
    import flask

    print(f"✅ Flask installed: version {flask.__version__}")
except ImportError as e:
    print(f"❌ Flask not installed: {e}")
    print("\n   FIX: Run 'pip install Flask'")
    sys.exit(1)

print()

# Try importing key AlphaVox modules
print("4. ALPHAVOX MODULE IMPORTS:")
print("-" * 80)

modules_to_test = [
    "app_init",
    "db",
    "conversation_engine",
    "learning_journey",
]

failed_imports = []

for module in modules_to_test:
    try:
        __import__(module)
        print(f"✅ {module}")
    except Exception as e:
        print(f"❌ {module}: {str(e)[:60]}")
        failed_imports.append((module, str(e)))

print()

# Check database
print("5. DATABASE CHECK:")
print("-" * 80)
if os.path.exists("alphavox.db"):
    size = os.path.getsize("alphavox.db")
    print(f"✅ Database exists ({size:,} bytes)")
else:
    print("⚠️  Database not found - will be created on first run")

print()

# Try to start a minimal Flask app
print("6. FLASK APP TEST:")
print("-" * 80)
print("Testing if Flask can start on port 5001...")

try:
    from flask import Flask

    test_app = Flask(__name__)

    @test_app.route("/")
    def home():
        return "Test OK"

    print("✅ Flask app created successfully")
    print("✅ Test route registered")

    # Check if port 5001 is available
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("127.0.0.1", 5001))
    sock.close()

    if result == 0:
        print("⚠️  Port 5001 is ALREADY IN USE!")
        print("   Another instance of AlphaVox may be running")
        print("   FIX: Kill the process or use a different port")
    else:
        print("✅ Port 5001 is available")

except Exception as e:
    print(f"❌ Error creating Flask app: {e}")
    import traceback

    traceback.print_exc()

print()

# Final recommendations
print("=" * 80)
print("DIAGNOSIS")
print("=" * 80)
print()

if failed_imports:
    print("❌ CRITICAL: Some modules failed to import:")
    for mod, error in failed_imports:
        print(f"   {mod}: {error}")
    print()
    print("FIX: Install missing dependencies:")
    print("   pip install -r requirements.txt")
    print()
else:
    print("✅ All modules imported successfully")
    print()

print("NEXT STEPS:")
print()
print("1. Make sure no other AlphaVox instances are running:")
print("   lsof -i :5001")
print("   (If something is running, kill it with: kill -9 <PID>)")
print()
print("2. Start AlphaVox with verbose output:")
print("   python app.py --port 5001")
print()
print("3. Watch for errors in the console")
print()
print("4. In another terminal, test the connection:")
print("   curl http://localhost:5001/")
print()
print("5. If you see HTML output, the server is running!")
print()
