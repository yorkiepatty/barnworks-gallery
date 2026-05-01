#!/usr/bin/env python3
"""
Quick test to see if learning routes can be imported and registered
"""

import sys
import traceback

print("Testing Learning Route Registration...")
print("=" * 50)

# Test basic imports first
print("\n1. Testing basic imports:")
try:
    from flask import Flask

    print("✅ Flask imports OK")
except Exception as e:
    print(f"❌ Flask import failed: {e}")
    sys.exit(1)

# Test the learning routes import
print("\n2. Testing learning routes import:")
try:
    from routes import register_learning_routes

    print("✅ register_learning_routes import OK")
except Exception as e:
    print(f"❌ register_learning_routes import failed: {e}")
    print("Full traceback:")
    traceback.print_exc()
    sys.exit(1)

# Test creating a test app and registering routes
print("\n3. Testing route registration:")
try:
    app = Flask(__name__)
    success = register_learning_routes(app)
    if success:
        print("✅ Learning routes registered successfully!")

        # List the registered routes
        print("\n4. Registered routes:")
        for rule in app.url_map.iter_rules():
            if "/learning" in str(rule):
                print(f"   {rule.methods} {rule.rule} -> {rule.endpoint}")

    else:
        print("❌ Learning route registration returned False")

except Exception as e:
    print(f"❌ Route registration failed: {e}")
    print("Full traceback:")
    traceback.print_exc()

print("\n" + "=" * 50)
print("Test complete")
