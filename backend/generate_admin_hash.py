#!/usr/bin/env python3
"""
© 2025 The Christman AI Project. All rights reserved.

Script to generate secure password hashes for admin users.
Use this to create ADMIN_PASSWORD_HASH for environment variables.

HIPAA Security Note: Never store plaintext passwords in any file or code.
Always use bcrypt hashes with proper salt rounds.
"""

import getpass
import secrets
import sys

import bcrypt


def generate_password_hash(password: str | None = None) -> str:
    """Generate bcrypt hash for a password."""
    if not password:
        password = getpass.getpass("Enter admin password: ")
        confirm = getpass.getpass("Confirm admin password: ")

        if password != confirm:
            print("❌ Passwords don't match!")
            sys.exit(1)

    # Use 12 rounds for production security
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

    return password_hash.decode("utf-8")


def generate_secure_username() -> str:
    """Generate a secure random username."""
    return f"admin_{secrets.token_hex(8)}"


if __name__ == "__main__":
    print("🔐 AlphaVox Admin Credential Generator")
    print("=" * 50)

    # Generate secure username
    username = generate_secure_username()
    print(f"✅ Generated username: {username}")

    # Generate password hash
    try:
        password_hash = generate_password_hash()
        print("✅ Generated password hash successfully")

        print("\n📝 Add these to your environment variables:")
        print(f"ADMIN_USERNAME={username}")
        print(f"ADMIN_PASSWORD_HASH={password_hash}")

        print("\n⚠️  SECURITY REMINDERS:")
        print("1. Never commit these values to git")
        print("2. Store in AWS Secrets Manager or Parameter Store")
        print("3. Rotate credentials every 90 days")
        print("4. Use different credentials for each environment")

    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

__all__ = ['generate_password_hash', 'generate_secure_username']
