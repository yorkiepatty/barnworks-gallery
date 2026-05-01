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

# /speech/transcriber.py
# Hybrid VOSK + AlphaVox speech recognition module

import json
import os
import queue

try:
    import sounddevice as sd
except ImportError:
    pass  # Optional dependency as sd
try:
    import vosk
except ImportError:
    pass  # Optional dependency

# Load AlphaVox custom vocabulary
with open("./speech/vocab-alpha.json", "r") as f:
    custom_vocab = json.load(f)

# Load VOSK model
MODEL_PATH = "./speech/vosk-model-small-en-us-0.15"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Download the VOSK model and place it in ./speech/")
model = vosk.Model(MODEL_PATH)

# Audio stream config
q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))


def recognize():
    print("🎤 Listening... Press Ctrl+C to stop.")
    with sd.RawInputStream(
        samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback
    ):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                raw_result = json.loads(rec.Result())
                text = raw_result.get("text", "").strip()
                if text:
                    corrected = postprocess(text)
                    print(f"🗣️  Heard: {text}\n🔧 Corrected: {corrected}\n")


# Post-process transcription
# Apply fixes, corrections, and AlphaVox logic


def postprocess(text):
    corrections = {
        "ice cream": "I scream",
        "no no": "no",
        "help me now": "emergency help",
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)

    # Custom terms reinforcement
    for term in custom_vocab.get("terms", []):
        if term["alias"] in text:
            text = text.replace(term["alias"], term["canonical"])
    return text


if __name__ == "__main__":
    try:
        recognize()
    except KeyboardInterrupt:
        print("\n🛑 Recognition stopped.")

# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['callback', 'recognize', 'postprocess']
