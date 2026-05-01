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
alphavox Dashboard - Main Entry Point
The Christman AI Project
Version: 1.0.0
"""

import logging
import os
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import boto3
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel

from alphavox_ultimate_voice import alphavoxUltimateVoice
from brain import alphavox_instance  # Use explicit instance for clarity
from conversation_engine import ConversationEngine
from memory_engine import MemoryEngine
from perplexity_service import PerplexityService

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Configure logging for HIPAA audit trails
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/alphavox_dashboard.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AlphaVox Dashboard", description="Voice for the voiceless")

# Initialize AlphaVox Ultimate Voice for synthesis
try:
    ultimate_voice = alphavoxUltimateVoice()
    logger.info("✅ alphavoxUltimateVoice initialized for AlphaVox")
except Exception as e:
    logger.error(f"❌ Failed to initialize alphavoxUltimateVoice: {str(e)}")
    # Continue without voice synthesis for now
    ultimate_voice = None

# Voice constants from alphavox_ultimate_voice
NEURAL_VOICES = {
    "matthew": {"name": "Matthew", "gender": "Male", "language": "en-US"},
    "joanna": {"name": "Joanna", "gender": "Female", "language": "en-US"},
    "stephen": {"name": "Stephen", "gender": "Male", "language": "en-GB"},
    "ruth": {"name": "Ruth", "gender": "Female", "language": "en-US"},
    "kevin": {"name": "Kevin", "gender": "Male", "language": "en-US"},
    "gregory": {"name": "Gregory", "gender": "Male", "language": "en-US"},
    "amy": {"name": "Amy", "gender": "Female", "language": "en-GB"},
}

# Simple memory storage for conversations
conversation_memory = []


# TTS Request Model
class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "Matthew"
    speed: Optional[float] = 1.0


class AlphaVoxDashboard:
    def __init__(self):
        logger.info("=" * 60)
        logger.info("🚀 Initializing AlphaVox Dashboard")
        logger.info("The Christman AI Project - AI That Empowers")
        logger.info("=" * 60)

        # Initialize components
        self.memory_engine: Optional[MemoryEngine] = None
        self.conversation_engine: Optional[ConversationEngine] = None
        self.perplexity_service: Optional[PerplexityService] = None
        self.alphavox = alphavox_instance  # Use explicit instance
        self.ultimate_voice = ultimate_voice

        self.api_host = "127.0.0.1"
        self.api_port = 8000

        self._initialize_components()

    def _initialize_components(self):
        logger.info("Loading memory engine...")
        memory_path = "./memory/memory_store.json"
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        try:
            self.memory_engine = MemoryEngine(file_path=memory_path)
            logger.info(f"Memory engine initialized with file: {memory_path}")
            self.conversation_engine = ConversationEngine()
            logger.info("Conversation engine initialized")
            try:
                self.perplexity_service = PerplexityService()
                logger.info("Perplexity service initialized")
            except Exception as e:
                logger.warning(f"Perplexity service not available: {str(e)}")
                self.perplexity_service = None
            logger.info("✓ All components initialized successfully")
        except Exception as e:
            logger.error(f"❌ Component initialization failed: {str(e)}")
            raise

    def start(self):
        logger.info("")
        logger.info("=" * 60)
        logger.info("🚀 Starting AlphaVox Dashboard Services")
        logger.info("=" * 60)
        logger.info("")
        try:
            logger.info("→ Starting AlphaVox learning system...")
            if self.alphavox:
                self.alphavox.start_learning()
            logger.info("→ Loading memory context...")
            if self.memory_engine:
                recent_events = self.memory_engine.get_recent_events()
                logger.info(f"Loaded {len(recent_events)} recent memory events")
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ AlphaVox Dashboard is RUNNING")
            logger.info("✓ Ready for conversation processing")
            logger.info("=" * 60)
            logger.info("")
            self._display_greeting()
        except Exception as e:
            logger.error(f"❌ Failed to start dashboard: {str(e)}")
            self.stop()
            sys.exit(1)

    def _display_greeting(self):
        if self.alphavox:
            greeting = self.alphavox.generate_greeting()
            logger.info(f"🗣️ AlphaVox says: {greeting}")
            # Speak the greeting using Ultimate Voice
            if self.ultimate_voice:
                self.ultimate_voice.speak(greeting)

    def process_message(self, message: str):
        if not self.alphavox:
            logger.warning("AlphaVox is not initialized yet.")
            return "System not ready."
        try:
            response = self.alphavox.think(message)
            response_text = response.get("response", "[No output]")

            # Speak the response using Ultimate Voice
            if self.ultimate_voice:
                self.ultimate_voice.speak(response_text)

            # Store conversation in simple memory
            conversation_memory.append(
                {
                    "input": message,
                    "output": response_text,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            return response_text
        except Exception as e:
            logger.error(f"Error during message processing: {str(e)}")
            return "Error processing message."

    def stop(self):
        logger.info("🧠 Shutting down AlphaVox Dashboard services...")
        try:
            if self.memory_engine:
                # Save last event for teaching
                self.memory_engine.save(
                    {"event": "shutdown", "timestamp": datetime.now().isoformat()}
                )
                logger.info("Memory engine saved successfully.")
        except Exception as e:
            logger.error(f"Error saving memory on shutdown: {str(e)}")
        logger.info("🛑 AlphaVox Dashboard stopped cleanly.")


# FastAPI TTS Endpoint
@app.post("/tts/synthesize")
async def synthesize_tts(request: TTSRequest = Body(...)):
    try:
        if not request.text or len(request.text) > 1000:
            raise HTTPException(status_code=400, detail="Text too long for real-time TTS")
        speed = request.speed if request.speed is not None else 1.0
        if not 0.5 <= speed <= 2.0:
            raise HTTPException(status_code=400, detail="Speed must be between 0.5 and 2.0")
        if request.voice not in NEURAL_VOICES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid voice: {request.voice}. Choose from {list(NEURAL_VOICES.keys())}",
            )

        # Use Ultimate Voice if available, otherwise fall back to basic synthesis
        if ultimate_voice:
            ultimate_voice.speak(request.text, voice=request.voice)
            logger.info(
                f"TTS synthesized via Ultimate Voice: {request.text[:50]}... (voice: {request.voice})"
            )
        else:
            # Fallback: Basic AWS Polly
            polly = boto3.client("polly")
            response = polly.synthesize_speech(
                Text=request.text,
                OutputFormat="mp3",
                VoiceId=str(request.voice).capitalize(),
                Engine="neural",
                SampleRate="22050",
            )
            temp_dir = tempfile.gettempdir()
            audio_file = os.path.join(temp_dir, f"alphavox_{uuid.uuid4()}.mp3")
            with open(audio_file, "wb") as f:
                f.write(response["AudioStream"].read())

            # Simple audio playback (would need platform-specific implementation)
            logger.info(f"Audio file created: {audio_file}")
            os.remove(audio_file)
            logger.info(
                f"TTS synthesized via Polly: {request.text[:50]}... (voice: {request.voice})"
            )

        # Store TTS interaction in simple memory
        conversation_memory.append(
            {
                "type": "tts",
                "text": request.text,
                "voice": request.voice,
                "speed": speed,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return {"status": "success", "text": request.text, "voice": request.voice}
    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")


@app.get("/health")
async def health_check():
    try:
        return {
            "status": "healthy",
            "conversation_count": len(conversation_memory),
            "ultimate_voice_available": ultimate_voice is not None,
            "message": "AlphaVox is ready to speak for the voiceless",
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}


def main():
    dashboard = None
    try:
        dashboard = AlphaVoxDashboard()
        dashboard.start()
        logger.info("Testing conversation system...")
        response = dashboard.process_message("Hello AlphaVox, how are you?")
        logger.info(f"Test response: {response}")
        logger.info("Dashboard running. Press Ctrl+C to stop.")
        import uvicorn

        uvicorn.run(
            app,
            host=os.getenv("ALPHAVOX_HOST", "127.0.0.1"),
            port=int(os.getenv("ALPHAVOX_PORT", "\1")),
        )
    except KeyboardInterrupt:
        logger.info("⌨️ Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        if dashboard:
            dashboard.stop()


if __name__ == "__main__":
    main()

__all__ = ['main', 'TTSRequest', 'AlphaVoxDashboard']
