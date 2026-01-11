from fastapi import APIRouter
import time

router = APIRouter()

START_TIME = time.time()

@router.get("/health")
def health_check() -> dict:
    """
    Health endpoint.
    Docstring for health_check
    
    :return: Server health status
    :rtype: dict
    """
    uptime_seconds = int(time.time() - START_TIME)
    return {
        "status": "ok", 
        "uptime_seconds": uptime_seconds, 
        "models_loaded": True,
    }
