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

# /speech/voice_diag.py

import os

try:
    import sounddevice as sd
except ImportError:
    pass  # Optional dependency as sd

print("\n🧪 alphavox Voice Diagnostic Starting\n")

# Check VOSK model path


def check_model_path():
    model_path = os.environ.get("VOSK_MODEL_PATH")
    if not model_path:
        print("❌ VOSK_MODEL_PATH not set.")
        return False
    if not os.path.exists(model_path):
        print(f"❌ Path does not exist: {model_path}")
        return False
    print(f"✅ VOSK_MODEL_PATH set and found: {model_path}")
    return True


# Check imports


def check_imports():
    for mod in ("vosk", "webrtcvad"):
        try:
            __import__(mod)
            print("✅ {} available".format(mod))
        except Exception:
            print("❌ {} not installed".format(mod))
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.say("test")
        engine.runAndWait()
        print("✅ pyttsx3 working")
    except ImportError:
        print("❌ pyttsx3 not installed")
    except Exception as e:
        print("❌ pyttsx3 error: {}".format(e))


def check_mic():
    try:
        devices = sd.query_devices()
        input_devices = [d for d in devices if d["max_input_channels"] > 0]
        if input_devices:
            print("✅ Microphone(s) found:")
            for idx, dev in enumerate(input_devices):
                print(f"   [{idx}] {dev['name']}")
        else:
            print("❌ No input devices found")
    except Exception as e:
        print(f"❌ Error accessing mic: {e}")


if __name__ == "__main__":
    check_model_path()
    check_imports()
    check_mic()
    print("\n✅ Diagnostic complete — review above results.")

# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['check_model_path', 'check_imports', 'check_mic']
