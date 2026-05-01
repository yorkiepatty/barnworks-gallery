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

import json
import os
from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from brain import (
    alphavox,
    speak_response,  # Import TTS function for health check
)

router = APIRouter()


router = APIRouter()


class CrawlInput(BaseModel):
    query: str


@router.post("/crawl_and_learn")
async def crawl_and_learn(payload: CrawlInput):
    """Web crawl + learn + summarize."""
    summary = alphavox._search_web(payload.query)
    return {"summary": summary}


class UserInput(BaseModel):
    input_text: str


class Status(BaseModel):
    mode: str
    emotion: str
    cognitive_load: int


@router.post("/alphavox/think")
async def alphavox_think(payload: UserInput):
    """
    Route user input through alphavox's brain and return the structured result.
    """
    input_text = payload.input_text
    result = alphavox.think(input_text)
    return result


@router.get("/speech/status")
async def speech_status():
    """
    Checks if the speech engine (TTS) is operational.
    """
    try:
        # Attempt a dry run of speak_response to confirm it's not a stub
        test_phrase = "Speech engine check passed."
        speak_response(test_phrase)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@router.get("/status", response_model=Status)
async def status_check():
    """
    Quick health check to see if alphavox is running with status, mode, emotion.
    """
    return Status(
        mode="architect",
        emotion="🙂 Focused",
        cognitive_load=42,
    )


@router.get("/learning/state")
async def get_learning_topic():
    curriculum_path = Path(__file__).resolve().parent / "data" / "curriculum.json"
    if curriculum_path.exists():
        with open(curriculum_path, "r") as f:
            data = json.load(f)
            return {"current_topic": data.get("current_topic", "Not specified")}
    return {"current_topic": "No curriculum file found"}


@router.get("/trending")
async def get_trending_topics():
    path = "./daily_summary.trending_topics"
    if os.path.exists(path):
        with open(path, "r") as f:
            topics = [line.strip() for line in f.readlines() if line.strip()]
            return {"topics": topics}
    return {"topics": ["No trending topics available"]}


@router.get("/memory/stats")
async def get_memory_stats():
    """
    Return basic stats from alphavox's memory engine.
    """
    if hasattr(alphavox, "memory_engine"):
        try:
            return {"total": alphavox.memory_engine.count()}
        except Exception as e:
            return {"error": str(e)}
    return {"error": "Memory engine not initialized."}


# Create app AFTER routes are defined
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.1.245:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(router)

# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
# Core Directive: "How can I help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================

__all__ = ['CrawlInput', 'UserInput', 'Status']
