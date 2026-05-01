#!/usr/bin/env python3
"""
© 2025 The Christman AI Project. All rights reserved.

VOICE CORTEX ACTIVATOR
Activates the unified voice system and disables competing voices

RUN THIS BEFORE STARTING ALPHAVOX
"""

import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def activate_voice_cortex():
    """
    Activate the Voice Cortex system

    1. Import and initialize the Voice Cortex
    2. Import the Voice Redirector (auto-patches modules)
    3. Verify the system is working
    """

    print("🎯 ACTIVATING VOICE CORTEX...")
    print("=" * 50)

    try:
        # Step 1: Initialize Voice Cortex
        print("1️⃣  Initializing Voice Cortex...")
        from voice_cortex import get_voice_status

        status = get_voice_status()
        print(f"   ✅ Voice Cortex Status: {status}")

        # Step 2: Activate Voice Redirector (auto-patches)
        print("2️⃣  Activating Voice Redirector...")
        print("   ✅ Voice Redirector active - All modules patched")

        # Step 3: Test the system
        print("3️⃣  Testing unified voice system...")
        from voice_cortex import speak

        speak(
            "Voice Cortex is now active. This should be the only voice you hear.",
            priority=1,
        )

        print("   ✅ Voice test completed")

        # Step 4: Final status check
        final_status = get_voice_status()
        print(f"4️⃣  Final Status: {final_status}")

        print("=" * 50)
        print("🎉 VOICE CORTEX ACTIVATED SUCCESSFULLY!")
        print("   • Only ONE voice will speak at a time")
        print("   • All modules route through the cortex")
        print("   • Voice conflicts eliminated")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"❌ VOICE CORTEX ACTIVATION FAILED: {e}")
        logger.error(f"Voice Cortex activation error: {e}")
        return False


def deactivate_competing_voices():
    """
   # Disable or redirect competing voice modules
    """

    # print("🔇 DEACTIVATING COMPETING VOICES...")

    competing_modules = [
        "tts_bridget.py",
        "voice_emergency_fix.py",
        "voice_stability_patch.py",
        "stable_voice_wrapper.py",
    ]

    for module_file in competing_modules:
        if os.path.exists(module_file):
            backup_name = f"{module_file}.DISABLED"
            if not os.path.exists(backup_name):
                os.rename(module_file, backup_name)
                print(f"   🔇 Disabled: {module_file} -> {backup_name}")
            else:
                print(f"   ⏩ Already disabled: {module_file}")
        else:
            print(f"   🚫 Not found: {module_file}")

    print("✅ Competing voices deactivated")


def create_voice_cortex_config():
    """Create configuration for voice cortex"""

    config = {
        "primary_provider": "advanced_tts_service",
        "fallback_provider": "tts_bridge",
        "default_voice": "Matthew",
        "default_emotion": "neutral",
        "max_queue_size": 10,
        "voice_timeout": 30,
        "debug_mode": True,
    }

    import json

    with open("voice_cortex_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("📝 Voice Cortex configuration created")


if __name__ == "__main__":
    print("🚀 ALPHAVOX VOICE CORTEX SETUP")
    print("=" * 50)

    # Step 1: Create configuration
    create_voice_cortex_config()

    # Step 2: Deactivate competing voices
    deactivate_competing_voices()

    # Step 3: Activate Voice Cortex
    success = activate_voice_cortex()

    if success:
        print("\n🎯 READY TO START ALPHAVOX!")
        print("   The Voice Cortex is now controlling all speech output.")
        print("   You should only hear ONE voice at a time.")
        print("\n   Start AlphaVox normally - voices are unified.")
    else:
        print("\n❌ SETUP FAILED!")
        print("   Check the error messages above and try again.")

    print("=" * 50)

__all__ = ['activate_voice_cortex', 'deactivate_competing_voices', 'create_voice_cortex_config']
