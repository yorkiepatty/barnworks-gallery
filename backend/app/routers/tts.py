"""
AlphaVox Text-to-Speech Router
AWS Polly primary · gTTS emergency fallback

ToneScore™ integration: emotion maps to SSML prosody (rate, pitch, volume)
so AlphaVox doesn't just say words — it expresses them.
"""

from __future__ import annotations

import io
import logging
import os
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()

# ── AWS Polly voice catalogue ─────────────────────────────────────────────────
# Neural engine voices — natural quality for AAC communication.
POLLY_VOICES = {
    # US English — neural
    "Joanna":  {"id": "Joanna",  "gender": "Female", "engine": "neural"},
    "Ruth":    {"id": "Ruth",    "gender": "Female", "engine": "neural"},
    "Matthew": {"id": "Matthew", "gender": "Male",   "engine": "neural"},
    "Stephen": {"id": "Stephen", "gender": "Male",   "engine": "neural"},
    "Kevin":   {"id": "Kevin",   "gender": "Male",   "engine": "neural"},  # child-appropriate
    # UK English — neural
    "Amy":     {"id": "Amy",     "gender": "Female", "engine": "neural"},
    "Brian":   {"id": "Brian",   "gender": "Male",   "engine": "neural"},
    # Standard (wider availability)
    "Salli":   {"id": "Salli",   "gender": "Female", "engine": "standard"},
    "Justin":  {"id": "Justin",  "gender": "Male",   "engine": "standard"},
}

DEFAULT_VOICE = os.getenv("POLLY_VOICE", "Joanna")

# ── ToneScore™ → SSML prosody mapping ────────────────────────────────────────
# Each emotion drives rate/pitch/volume in the SSML wrapper.
EMOTION_PROSODY: dict[str, dict] = {
    "calm":        {"rate": "slow",    "pitch": "-2st",  "volume": "soft"},
    "warm":        {"rate": "medium",  "pitch": "+0st",  "volume": "medium"},
    "gentle":      {"rate": "slow",    "pitch": "-1st",  "volume": "soft"},
    "excited":     {"rate": "fast",    "pitch": "+4st",  "volume": "loud"},
    "celebratory": {"rate": "fast",    "pitch": "+5st",  "volume": "loud"},
    "urgent":      {"rate": "medium",  "pitch": "+2st",  "volume": "loud"},
    "distressed":  {"rate": "slow",    "pitch": "-1st",  "volume": "soft"},
    "playful":     {"rate": "fast",    "pitch": "+3st",  "volume": "medium"},
    "serious":     {"rate": "medium",  "pitch": "-3st",  "volume": "medium"},
    "sad":         {"rate": "slow",    "pitch": "-4st",  "volume": "soft"},
}


def _wrap_ssml(text: str, emotion: Optional[str]) -> str:
    prosody = EMOTION_PROSODY.get(emotion or "warm", EMOTION_PROSODY["warm"])
    return (
        "<speak>"
        f'<prosody rate="{prosody["rate"]}" pitch="{prosody["pitch"]}" volume="{prosody["volume"]}">'
        f"{text}"
        "</prosody>"
        "</speak>"
    )


# ── Request model ─────────────────────────────────────────────────────────────

class TTSRequest(BaseModel):
    text:    str
    voice:   Optional[str]  = DEFAULT_VOICE
    emotion: Optional[str]  = "warm"
    speed:   Optional[float] = 1.0


# ── Primary: AWS Polly ────────────────────────────────────────────────────────

async def _synthesize_polly(request: TTSRequest) -> bytes:
    import boto3
    voice_cfg = POLLY_VOICES.get(request.voice or DEFAULT_VOICE, POLLY_VOICES[DEFAULT_VOICE])
    engine    = voice_cfg["engine"]
    ssml_text = _wrap_ssml(request.text, request.emotion)

    polly = boto3.client("polly", region_name=os.getenv("AWS_REGION", "us-east-1"))
    response = polly.synthesize_speech(
        TextType="ssml",
        Text=ssml_text,
        OutputFormat="mp3",
        VoiceId=voice_cfg["id"],
        Engine=engine,
    )
    return response["AudioStream"].read()


# ── Fallback: gTTS ────────────────────────────────────────────────────────────

async def _synthesize_gtts(text: str) -> bytes:
    from gtts import gTTS
    buf = io.BytesIO()
    gTTS(text=text, lang="en", slow=False).write_to_fp(buf)
    buf.seek(0)
    return buf.read()


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/synthesize")
async def synthesize_tts(request: TTSRequest):
    """
    Synthesize speech from text.

    Priority chain:
      1. AWS Polly  (primary — neural voices, SSML/ToneScore™ support)
      2. gTTS       (emergency — always available, no credentials needed)
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if len(request.text) > 2500:
        raise HTTPException(status_code=400, detail="Text too long (max 2500 chars)")

    audio_bytes: Optional[bytes] = None
    source = "unknown"

    try:
        audio_bytes = await _synthesize_polly(request)
        source = "polly"
        logger.info("TTS via Polly [%s chars, voice=%s, emotion=%s]",
                    len(request.text), request.voice, request.emotion)
    except Exception as exc:
        logger.warning("Polly TTS failed, falling back to gTTS: %s", exc)
        try:
            audio_bytes = await _synthesize_gtts(request.text)
            source = "gtts"
            logger.info("TTS via gTTS fallback [%s chars]", len(request.text))
        except Exception as exc2:
            logger.error("gTTS fallback also failed: %s", exc2)
            raise HTTPException(status_code=503, detail="All TTS providers unavailable") from exc2

    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers={
            "X-TTS-Source": source,
            "X-Voice-Name": request.voice or DEFAULT_VOICE,
            "Content-Disposition": "inline; filename=alphavox_speech.mp3",
        },
    )


@router.get("/voices")
async def list_voices():
    """List all available Polly voices."""
    voices = [
        {
            "name":            name,
            "voice_id":        cfg["id"],
            "gender":          cfg["gender"],
            "engine":          cfg["engine"],
            "source":          "polly",
            "suitable_for_aac": True,
        }
        for name, cfg in POLLY_VOICES.items()
    ]
    return {"voices": voices, "default": DEFAULT_VOICE}


@router.get("/voices/{voice_id}/preview")
async def preview_voice(voice_id: str):
    """Generate a short preview of a voice."""
    req = TTSRequest(text="Hello. I'm AlphaVox. I'm here to help you communicate.",
                     voice=voice_id, emotion="warm")
    return await synthesize_tts(req)
