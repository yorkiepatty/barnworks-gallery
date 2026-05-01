#!/usr/bin/env python3
"""Quick voice test to verify stability"""

import runpy
import sys

sys.path.insert(0, ".")


def test_voice_stability():
    try:
        from alphavox_ultimate_voice import alphavoxUltimateVoice

        print("🧪 Testing voice stability...")
        voice_system = alphavoxUltimateVoice()

        # Apply stability patch
        runpy.run_path("voice_stability_patch.py")

        test_phrases = [
            "Testing voice consistency - phrase one",
            "Testing voice consistency - phrase two",
            "Testing voice consistency - phrase three",
        ]

        print(f"Locked to voice: {voice_system.default_voice}")

        for i, phrase in enumerate(test_phrases, 1):
            print(f"\nTest {i}/3:")
            success = voice_system.speak(phrase)
            if success:
                print(f"✅ Consistent voice output {i}")
            else:
                print(f"❌ Voice output failed {i}")

        print("\n🎉 Voice stability test complete!")

    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    test_voice_stability()

__all__ = ['test_voice_stability']
