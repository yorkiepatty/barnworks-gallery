"""Input processing endpoint – routes user text/voice input through the brain."""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()


class InputRequest(BaseModel):
    text: str
    user_id: Optional[str] = "anonymous"
    input_type: Optional[str] = "text"


@router.post("/process-input")
async def process_input(request: InputRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="No input provided")

    try:
        from brain import alphavox_instance  # type: ignore

        result = alphavox_instance.process(
            {"type": request.input_type, "input": request.text},
            request.user_id,
        )
        return result
    except ImportError:
        logger.warning("Brain module not available – returning echo response")
        return {
            "status": "ok",
            "message": f"Echo: {request.text}",
            "user_id": request.user_id,
        }
    except Exception as exc:
        logger.error("Input processing error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
