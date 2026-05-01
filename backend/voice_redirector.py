"""
© 2025 The Christman AI Project. All rights reserved.

VOICE REDIRECTOR - Redirect all speak functions to Voice Cortex

This module replaces all existing speak functions and redirects them
to the Voice Cortex for unified control.

STOPS THE VOICE CHAOS.
"""

import logging
from typing import Optional

from voice_cortex import speak as cortex_speak

logger = logging.getLogger(__name__)

# =============================================================================
# GLOBAL SPEAK FUNCTIONS - ALL ROUTE TO VOICE CORTEX
# =============================================================================

def speak(text: str, voice: Optional[str] = None, emotion: str = "neutral") -> bool:
    """Universal speak function - redirects to Voice Cortex"""
    logger.info(f"🔀 Redirecting to Voice Cortex: {text[:50]}...")
    return cortex_speak(text, voice, emotion)


def speak_response(text: str) -> None:
    """TTS Bridge compatibility - redirects to Voice Cortex"""
    cortex_speak(text)


def text_to_speech(text: str, emotion=None, emotion_tier=None, voice_id="matthew") -> str:
    """App.py compatibility - redirects to Voice Cortex"""
    cortex_speak(text, voice_id, emotion)
    return "Voice Cortex handled speech"


def text_to_speech_with_emotion(text: str, emotion=None, voice_id="matthew", **kwargs) -> str:
    """Advanced TTS compatibility - redirects to Voice Cortex"""
    cortex_speak(text, voice_id, emotion)
    return "Voice Cortex handled speech"


def speak_text():
    """Placeholder for Flask routes - use cortex_speak() instead"""
    return {"status": "Use voice_cortex.speak() instead"}


def speak_greeting():
    """Placeholder for Flask routes - use cortex_speak() instead"""
    return {"status": "Use voice_cortex.speak() instead"}


def speak_with_emotion(text: str, emotion: str = "neutral", voice: Optional[str] = None, **kwargs):
    """Voice synthesis compatibility - redirects to Voice Cortex"""
    cortex_speak(text, voice, emotion)


# =============================================================================
# MONKEY PATCH EXISTING MODULES
# =============================================================================


def patch_all_voice_modules():
    """
    Replace speak functions in all modules with Voice Cortex redirects

    This ensures ALL voice output goes through the cortex.
    """

    modules_to_patch = [
        "app",
        "brain",
        "tts_bridge",
        "advanced_tts_service",
        "voice_synthesis",
        "speech_response",
        "alphavox_ultimate_voice",
        "emergency_derek_fix",
        "voice_emergency_fix",
        "stable_voice_wrapper",
    ]

    for module_name in modules_to_patch:
        try:
            import importlib

            module = importlib.import_module(module_name)

            # Replace common speak function names
            if hasattr(module, "speak"):
                setattr(module, "speak", speak)
                logger.info(f"✅ Patched {module_name}.speak()")

            if hasattr(module, "speak_response"):
                setattr(module, "speak_response", speak_response)
                logger.info(f"✅ Patched {module_name}.speak_response()")

            if hasattr(module, "text_to_speech"):
                setattr(module, "text_to_speech", text_to_speech)
                logger.info(f"✅ Patched {module_name}.text_to_speech()")

            if hasattr(module, "text_to_speech_with_emotion"):
                setattr(module, "text_to_speech_with_emotion", text_to_speech_with_emotion)
                logger.info(f"✅ Patched {module_name}.text_to_speech_with_emotion()")

        except ImportError:
            logger.debug(f"⏩ Module {module_name} not found, skipping patch")
        except Exception as e:
            logger.error(f"❌ Failed to patch {module_name}: {e}")

    logger.info("🎯 Voice module patching complete - All voices route to Cortex")


# Auto-patch when imported
patch_all_voice_modules()

if __name__ == "__main__":
    print("🔧 Testing Voice Redirector...")

    # Test all the redirect functions
    speak("Testing universal speak function")
    speak_response("Testing TTS bridge compatibility")
    text_to_speech("Testing app.py compatibility")
    text_to_speech_with_emotion("Testing advanced TTS compatibility")

    print("✅ Voice Redirector test complete")

__all__ = ['speak', 'speak_response', 'text_to_speech', 'text_to_speech_with_emotion', 'speak_text', 'speak_greeting', 'speak_with_emotion', 'patch_all_voice_modules']
