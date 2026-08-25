"""
Health Check Endpoint
"""
from fastapi import APIRouter

from backend.api.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        HealthResponse: Status object with 'ok' status
    """
    return HealthResponse(status="ok")
