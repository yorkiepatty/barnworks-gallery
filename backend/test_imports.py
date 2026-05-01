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
Quick module tester - Test import of all core modules
"""

import sys

modules_to_test = [
    "app_init",
    "models",
    "nonverbal_engine",
    "eye_tracking_service",
    "sound_recognition_service",
    "learning_analytics",
    "behavior_capture",
    "alphavox_input_nlu",
    "advanced_tts_service",
    "conversation_engine",
    "memory_engine",
    "ai_learning_engine",
    "neural_learning_core",
]

print("Testing module imports...")
failed = []
for module in modules_to_test:
    try:
        __import__(module)
        print(f"✓ {module}")
    except Exception as e:
        print(f"✗ {module}: {e}")
        failed.append(module)

print(f"\n{len(modules_to_test) - len(failed)}/{len(modules_to_test)} modules loaded successfully")
sys.exit(len(failed))
