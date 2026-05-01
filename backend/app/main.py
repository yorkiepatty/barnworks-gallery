"""
© 2025 The Christman AI Project. All rights reserved.

AlphaVox – FastAPI Backend Entry Point
Unified API surface for the Vite/React frontend.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ── Environment ─────────────────────────────────────────────────────────────
load_dotenv()

# Add backend root to path so all legacy modules resolve
BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

# ── Logging ──────────────────────────────────────────────────────────────────
os.makedirs(BACKEND_ROOT / "logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s – %(message)s",
    handlers=[
        logging.FileHandler(BACKEND_ROOT / "logs" / "alphavox_api.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AlphaVox API",
    description="Voice for the voiceless – FastAPI backend",
    version="2.0.0",
)

# Allow the Vite dev server (port 5173) and production origin
ALLOWED_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000,https://thechristmanaiproject.com,https://www.thechristmanaiproject.com,https://alphavox.thechristmanaiproject.com",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
from app.routers import health, input_processing, tts, memory as memory_router  # noqa: E402
from compliance_middleware import ComplianceMiddleware  # noqa: E402

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(tts.router, prefix="/api/tts", tags=["tts"])
app.include_router(input_processing.router, prefix="/api", tags=["input"])
app.include_router(memory_router.router, prefix="/api/memory", tags=["memory"])

app.add_middleware(ComplianceMiddleware)

logger.info("AlphaVox API ready")
logger.info("HIPAA/FDA compliance middleware active")

# Serve React frontend — must be after all API routers
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/", include_in_schema=False)
    async def serve_root():
        return FileResponse(str(FRONTEND_DIST / "index.html"))

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        index = FRONTEND_DIST / "index.html"
        return FileResponse(str(index))
else:
    logger.warning("Frontend dist not found at %s — UI will not be served", FRONTEND_DIST)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=os.getenv("ALPHAVOX_HOST", "0.0.0.0"),
        port=int(os.getenv("ALPHAVOX_PORT", "8000")),
        reload=True,
    )
