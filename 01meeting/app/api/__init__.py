from fastapi import APIRouter
from .endpoints import meetings

router = APIRouter()

# Include sub-routers
router.include_router(meetings.router)


@router.get("/status")
async def api_status():
    return {"status": "ok", "message": "API is running"}
