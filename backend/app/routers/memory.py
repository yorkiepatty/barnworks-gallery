"""Memory mesh endpoints."""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()


class MemoryStoreRequest(BaseModel):
    content: str
    category: Optional[str] = "general"
    importance: Optional[float] = 0.5


@router.get("/stats")
async def memory_stats():
    try:
        from memory_mesh_bridge import MemoryMeshBridge  # type: ignore

        bridge = MemoryMeshBridge(memory_dir="./alphavox_memory")
        return bridge.get_memory_stats()
    except Exception as exc:
        logger.warning("Memory stats unavailable: %s", exc)
        return {"status": "unavailable", "reason": str(exc)}


@router.post("/store")
async def store_memory(request: MemoryStoreRequest):
    try:
        from memory_mesh_bridge import MemoryMeshBridge  # type: ignore

        bridge = MemoryMeshBridge(memory_dir="./alphavox_memory")
        bridge.store(
            content=request.content,
            category=request.category,
            importance=request.importance,
        )
        return {"status": "stored"}
    except Exception as exc:
        logger.error("Memory store error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
