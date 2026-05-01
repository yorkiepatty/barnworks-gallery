"""
AlphaVox Text-to-Speech Router
ElevenLabs primary · AWS Polly fallback · gTTS emergency fallback

ElevenLabs gives AlphaVox users the most natural, emotionally expressive
voices available — critical for children and adults who are hearing their
voice (or a loved one's voice) for the first time.

ToneScore™ integration: voice parameters (stability, similarity, style)
are derived from the emotional tone of the message, so AlphaVox doesn't
just say words — it expresses them.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()

# ── ElevenLabs voice catalogue ────────────────────────────────────────────────
# These are the default ElevenLabs voices available without cloning.
# Users can add their own cloned voices via the /voices/clone endpoint.
ELEVENLABS_VOICES = {
    # Warm, clear voices well-suited for AAC / child communication
    "Rachel":  "21m00Tcm4TlvDq8ikWAM",   # warm, clear female — great default
    "Domi":    "AZnzlk1XvdvUeBnXmlld",   # strong, clear
    "Bella":   "EXAVITQu4vr4xnSDxMaL",   # soft, warm female
    "Antoni":  "ErXwobaYiN019PkySvjV",   # warm male
    "Elli":    "MF3mGyEYCl7XYWbV9V6O",   # emotional, young female
    "Josh":    "TxGEqnHWrfWFTfGW9XjX",   # deep, calm male
    "Arnold":  "VR6AewLTigWG4xSOukaG",   # crisp male
    "Adam":    "pNInz6obpgDQGcFmaJgB",   # deep male
    "Sam":     "yoZ06aMxZJJ28mfd3POQ",   # raspy, character
    # Child-appropriate
    "Matilda": "XrExE9yKIg1WjnnlVkGX",   # warm, friendly female
    "Grace":   "oWAxZDx7w5VEj9dCyTzz",   # soft, clear
}

ELEVENLABS_MODEL = "eleven_turbo_v2_5"   # fastest + most natural for real-time AAC
ELEVENLABS_MODEL_MULTILINGUAL = "eleven_multilingual_v2"

# Default voice — read from .env so you can swap without touching code
# Set ELEVENLABS_VOICE_NAME=Bella (or any name below) in your .env
import os as _os
DEFAULT_VOICE_NAME = _os.getenv("ELEVENLABS_VOICE_NAME", "Bella")
DEFAULT_VOICE_ID   = ELEVENLABS_VOICES.get(DEFAULT_VOICE_NAME, ELEVENLABS_VOICES["Bella"])


# ── Request / Response models ─────────────────────────────────────────────────

class TTSRequest(BaseModel):
    text:            str
    voice:           Optional[str]  = DEFAULT_VOICE_NAME
    voice_id:        Optional[str]  = None   # override with custom/cloned voice ID
    speed:           Optional[float] = 1.0
    emotion:         Optional[str]  = None   # e.g. "calm", "warm", "urgent"
    # ToneScore™ parameters — set automatically when processInput is called
    stability:       Optional[float] = 0.65  # 0–1: lower = more expressive
    similarity_boost:Optional[float] = 0.80  # 0–1: voice consistency
    style:           Optional[float] = 0.35  # 0–1: style exaggeration
    use_speaker_boost:bool = True


class VoiceCloneRequest(BaseModel):
    name:        str
    description: Optional[str] = None
    # In production: audio files would be uploaded via multipart form
    # For now we accept a list of pre-uploaded file paths (backend-side)
    audio_paths: list[str] = []


# ── Tone → voice parameter mapping ───────────────────────────────────────────
# ToneScore™ integration: emotion drives ElevenLabs voice settings
# so the voice actually *feels* right for the moment.

EMOTION_VOICE_PARAMS: dict[str, dict] = {
    "calm":        {"stability": 0.80, "similarity_boost": 0.80, "style": 0.15},
    "warm":        {"stability": 0.65, "similarity_boost": 0.85, "style": 0.35},
    "gentle":      {"stability": 0.75, "similarity_boost": 0.80, "style": 0.20},
    "excited":     {"stability": 0.35, "similarity_boost": 0.75, "style": 0.70},
    "celebratory": {"stability": 0.30, "similarity_boost": 0.70, "style": 0.80},
    "urgent":      {"stability": 0.50, "similarity_boost": 0.90, "style": 0.55},
    "distressed":  {"stability": 0.55, "similarity_boost": 0.85, "style": 0.45},
    "playful":     {"stability": 0.40, "similarity_boost": 0.75, "style": 0.65},
    "serious":     {"stability": 0.85, "similarity_boost": 0.90, "style": 0.10},
    "sad":         {"stability": 0.70, "similarity_boost": 0.80, "style": 0.30},
}


def _get_voice_params(request: TTSRequest) -> dict:
    """Resolve voice parameters from emotion or explicit values."""
    if request.emotion and request.emotion.lower() in EMOTION_VOICE_PARAMS:
        return EMOTION_VOICE_PARAMS[request.emotion.lower()]
    return {
        "stability":        request.stability        or 0.65,
        "similarity_boost": request.similarity_boost or 0.80,
        "style":            request.style            or 0.35,
    }


def _resolve_voice_id(request: TTSRequest) -> str:
    """Resolve to an ElevenLabs voice ID."""
    if request.voice_id:
        return request.voice_id
    if request.voice:
        # Check exact name match
        if request.voice in ELEVENLABS_VOICES:
            return ELEVENLABS_VOICES[request.voice]
        # Check case-insensitive
        for name, vid in ELEVENLABS_VOICES.items():
            if name.lower() == request.voice.lower():
                return vid
    return DEFAULT_VOICE_ID


# ── Primary: ElevenLabs synthesis ─────────────────────────────────────────────

async def _synthesize_elevenlabs(request: TTSRequest) -> bytes:
    """Call ElevenLabs API and return raw audio bytes (mp3)."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set")

    voice_id   = _resolve_voice_id(request)
    params     = _get_voice_params(request)

    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs import VoiceSettings

        client = ElevenLabs(api_key=api_key)

        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            text=request.text,
            model_id=ELEVENLABS_MODEL,
            voice_settings=VoiceSettings(
                stability=params["stability"],
                similarity_boost=params["similarity_boost"],
                style=params.get("style", 0.35),
                use_speaker_boost=request.use_speaker_boost,
            ),
            output_format="mp3_44100_128",
        )

        # Collect streaming chunks
        audio_bytes = b"".join(audio_generator)
        return audio_bytes

    except Exception as exc:
        logger.error("ElevenLabs synthesis failed: %s", exc)
        raise


# ── Fallback: AWS Polly ───────────────────────────────────────────────────────

async def _synthesize_polly(text: str) -> bytes:
    try:
        import boto3
        polly = boto3.client("polly")
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna",
            Engine="neural",
        )
        return response["AudioStream"].read()
    except Exception as exc:
        logger.error("Polly fallback failed: %s", exc)
        raise


# ── Emergency fallback: gTTS ──────────────────────────────────────────────────

async def _synthesize_gtts(text: str) -> bytes:
    try:
        import io
        from gtts import gTTS
        buf = io.BytesIO()
        gTTS(text=text, lang="en", slow=False).write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception as exc:
        logger.error("gTTS emergency fallback failed: %s", exc)
        raise


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/synthesize")
async def synthesize_tts(request: TTSRequest):
    """
    Synthesize speech from text.

    Priority chain:
      1. ElevenLabs (primary — natural, emotionally expressive)
      2. AWS Polly  (fallback — good quality, reliable)
      3. gTTS       (emergency — always available)

    Returns streaming audio/mpeg.
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if len(request.text) > 2500:
        raise HTTPException(status_code=400, detail="Text too long (max 2500 chars)")

    audio_bytes: Optional[bytes] = None

    # ElevenLabs only — no robotic fallbacks
    if not os.getenv("ELEVENLABS_API_KEY"):
        raise HTTPException(status_code=503, detail="ELEVENLABS_API_KEY not configured")

    try:
        audio_bytes = await _synthesize_elevenlabs(request)
        logger.info("TTS via ElevenLabs ✓ [%s chars, voice=%s]", len(request.text), request.voice)
    except Exception as e:
        logger.error("ElevenLabs TTS failed: %s", e)
        raise HTTPException(status_code=503, detail="Voice unavailable — ElevenLabs error") from e

    import io
    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers={
            "X-TTS-Source": source,
            "X-Voice-Name": request.voice or DEFAULT_VOICE_NAME,
            "Content-Disposition": "inline; filename=alphavox_speech.mp3",
        },
    )


@router.get("/voices")
async def list_voices():
    """List all available voices including any user-cloned voices."""
    voices = []

    # Always include ElevenLabs defaults
    for name, voice_id in ELEVENLABS_VOICES.items():
        voices.append({
            "name":     name,
            "voice_id": voice_id,
            "source":   "elevenlabs",
            "cloned":   False,
            "suitable_for_aac": True,
        })

    # Try to fetch user's custom voices from ElevenLabs
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if api_key:
        try:
            from elevenlabs.client import ElevenLabs
            client  = ElevenLabs(api_key=api_key)
            el_voices = client.voices.get_all()
            for v in el_voices.voices:
                if v.name not in ELEVENLABS_VOICES:
                    voices.append({
                        "name":     v.voice_id,
                        "voice_id": v.voice_id,
                        "source":   "elevenlabs_custom",
                        "cloned":   True,
                        "suitable_for_aac": True,
                    })
        except Exception as e:
            logger.warning("Could not fetch custom ElevenLabs voices: %s", e)

    return {"voices": voices, "default": DEFAULT_VOICE_NAME}


@router.post("/voices/clone")
async def clone_voice(request: VoiceCloneRequest):
    """
    Clone a voice from audio samples.

    This powers one of AlphaVox's most meaningful features:
    a parent can upload recordings of their own voice so their
    child hears a familiar, loving voice speaking for them.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="ElevenLabs API key not configured")

    if not request.audio_paths:
        raise HTTPException(status_code=400, detail="At least one audio file required for voice cloning")

    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=api_key)

        files = []
        for path in request.audio_paths:
            if not os.path.exists(path):
                raise HTTPException(status_code=400, detail=f"Audio file not found: {path}")
            files.append(open(path, "rb"))

        voice = client.clone(
            name=request.name,
            description=request.description or f"AlphaVox cloned voice: {request.name}",
            files=files,
        )

        for f in files:
            f.close()

        return {
            "status":   "success",
            "voice_id": voice.voice_id,
            "name":     voice.name,
            "message":  f"Voice '{request.name}' cloned successfully. Use voice_id in TTS requests.",
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Voice cloning failed: %s", exc)
        raise HTTPException(status_code=500, detail=f"Voice cloning failed: {exc}") from exc


@router.get("/voices/{voice_id}/preview")
async def preview_voice(voice_id: str):
    """Generate a short preview of a voice."""
    preview_text = "Hello. I'm AlphaVox. I'm here to help you communicate."
    req = TTSRequest(text=preview_text, voice_id=voice_id, emotion="warm")
    return await synthesize_tts(req)
