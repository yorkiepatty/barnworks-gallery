#!/usr/bin/env python3
"""
Emergency AlphaVox Startup - Stable Voice Mode
"""

import os
import sys

sys.path.insert(0, ".")

# Set environment for stability
os.environ["DISABLE_API_WARNINGS"] = "true"
os.environ["VOICE_LOCK"] = "matthew"
os.environ["PREVENT_VOICE_SWITCHING"] = "true"

print("🎤 Starting AlphaVox in STABLE VOICE MODE")
print("   Voice locked: matthew")
print("   API warnings: disabled")
print("   Switching prevention: enabled")
print()

try:
    # Import new Voice Cortex speaker
    from voice_cortex import speak

    # Import and patch main app
    import app

    # Override voice functions in app
    if hasattr(app, "ultimate_voice"):
        app.ultimate_voice.speak = speak
        print("✅ Voice override applied to ultimate_voice via voice_cortex")

    print("✅ AlphaVox starting with stable voice...")
    print("   Navigate to: http://localhost:5000")
    print()

    # Start the app
    if __name__ == "__main__":
        app.app.run(
            host=os.getenv("ALPHAVOX_HOST", "127.0.0.1"),
            port=int(os.getenv("ALPHAVOX_PORT", "5000")),
            debug=(os.getenv("ALPHAVOX_DEBUG", "0") == "1"),
        )

except Exception as e:
    print(f"❌ Startup error: {e}")
    print("\nTrying basic mode...")

    # Basic fallback
    print("\n[AlphaVox Emergency Mode]")
    print("Voice: matthew (locked)")
    print("Status: Ready for communication")

    # Simple loop
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["quit", "exit"]:
                break
            print(
                f"alphavox (matthew): I hear you saying '{user_input}'. I'm in stable voice mode."
            )
        except KeyboardInterrupt:
            break

    print("\nGoodbye!")
