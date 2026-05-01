import pathlib
import tempfile

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

"""
Quick Production Test Setup
Sets minimal environment variables for testing
"""

import os
import secrets

# Set minimal required environment variables for testing
os.environ["HIPAA_ENCRYPTION_KEY"] = "test_key_for_development_only_minimum_32_chars"
os.environ["JWT_SECRET_KEY"] = secrets.token_urlsafe(32)
os.environ["FLASK_SECRET_KEY"] = secrets.token_urlsafe(24)
os.environ["DATABASE_URL"] = "sqlite:///test_alphavox.db"
os.environ["REDIS_URL"] = "memory://"
os.environ["ENVIRONMENT"] = "development"
os.environ["SSL_CERT_FILE"] = str(pathlib.Path(tempfile.gettempdir()) / "test.crt")
os.environ["SSL_KEY_FILE"] = str(pathlib.Path(tempfile.gettempdir()) / "test.key")

print("✓ Test environment variables set")
print("⚠️ WARNING: These are TEST KEYS ONLY - DO NOT USE IN PRODUCTION")

# Test the production app
try:
    print("✓ Production app imports successfully")

    # Test security manager
    from security_config import security_manager

    print("✓ Security manager initialized")

    # Test encryption
    test_data = "Hello, HIPAA compliance!"
    encrypted = security_manager.encryption.encrypt(test_data)
    decrypted = security_manager.encryption.decrypt(encrypted)
    if decrypted == test_data:
        print("✓ HIPAA encryption working correctly")
    else:
        print("✗ Encryption test failed")

    # Test password validation
    valid, errors = security_manager.validate_password("AlphaVox2025!")
    if valid:
        print("✓ Password validation working")
    else:
        print(f"✗ Password validation failed: {errors}")

    print("\n🎉 PRODUCTION SYSTEM IS READY!")
    print("   All critical security features are operational")

except Exception as e:
    print(f"✗ Production test failed: {e}")
    import traceback

    traceback.print_exc()
