from dotenv import load_dotenv

load_dotenv()

"""
© 2025 The Christman AI Project. All rights reserved.

This code is released as part of a trauma-informed, dignity-first AI ecosystem designed to protect, empower, and elevate vulnerable populations.

By using, modifying, or distributing this software, you agree to uphold the following core principles:

1. Truth — No deception, no manipulation. Use this code honestly.
2. Dignity — Respect the autonomy, privacy, and humanity of all users.
3. Protection — This software must never be used to harm, exploit, or surveil vulnerable individuals.
4. Transparency — You must disclose modifications and contributions clearly.
5. No Erasure — Do not remove the origins, mission, or ethical foundation of this work.

This is not just code. It is redemption in code.

For questions or licensing requests, contact:
Everett N. Christman
📧 lumacognify@thechristmanaiproject.com
🌐 https://thechristmanaiproject.com

AlphaVox Dashboard - Unified Main Entry Point
Version: 1.0.0
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import what's available, handle missing imports gracefully
try:
    from alphavox import AlphaVoxUltimateVoice
except ImportError:
    AlphaVoxUltimateVoice = None

from brain import alphavox_instance
from conversation_engine import ConversationEngine
from memory_engine import MemoryEngine
from memory_mesh_bridge import MemoryMeshBridge

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

# Initialize AlphaVox voice
alphavox = None
if AlphaVoxUltimateVoice is not None:
    try:
        alphavox = AlphaVoxUltimateVoice()
        logger.info("✅ AlphaVoxUltimateVoice initialized for AlphaVox")
    except Exception as e:
        logger.error(f"❌ Failed to initialize AlphaVoxUltimateVoice: {str(e)}")
        alphavox = None
else:
    logger.warning("AlphaVoxUltimateVoice not available")

# Fallback: Initialize Ultimate Voice
ultimate_voice = None
try:
    from alphavox_ultimate_voice import alphavoxUltimateVoice
    ultimate_voice = alphavoxUltimateVoice()
    logger.info("✅ alphavoxUltimateVoice initialized")
except Exception as e:
    logger.warning(f"Fallback voice synthesis unavailable: {str(e)}")

# Initialize MemoryMeshBridge
memory = None
try:
    memory = MemoryMeshBridge(memory_dir="./alphavox_memory")
    logger.info("🧠 MemoryMeshBridge initialized")
except Exception as e:
    logger.error(f"❌ MemoryMeshBridge init failed: {str(e)}")

# TTS is handled by app/routers/tts.py (ElevenLabs) via app/main.py


@app.get("/health")
async def health_check():
    try:
        stats = memory.get_memory_stats() if memory else {}
        return {
            "status": "healthy",
            "memory_stats": stats,
            "ultimate_voice_available": ultimate_voice is not None,
            "message": "AlphaVox is ready to speak for the voiceless",
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}


def main():
    try:
        logger.info("🚀 Launching AlphaVox unified dashboard")
        from uvicorn import run

        run(
            app,
            host=os.getenv("ALPHAVOX_HOST", "127.0.0.1"),
            port=int(os.getenv("ALPHAVOX_PORT", "8000")),
        )
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()

__all__ = ['main']
