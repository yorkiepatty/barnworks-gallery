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
Simplified env loader for AlphaVox
"""

import os

from dotenv import load_dotenv


def LoadEnv():
    """Load environment variables from .env files."""
    # Load from .env.production if it exists, otherwise .env
    if os.path.exists(".env.production"):
        load_dotenv(".env.production")
    elif os.path.exists(".env"):
        load_dotenv(".env")
    return True

__all__ = ['LoadEnv']
