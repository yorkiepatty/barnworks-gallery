from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AlphaVox API",
        "message": "Voice for the voiceless",
    }
