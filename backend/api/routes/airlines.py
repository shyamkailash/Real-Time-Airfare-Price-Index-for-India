"""
Airlines API routes.
Provides endpoints for airline information.
"""
from fastapi import APIRouter
from typing import List

from backend.api.schemas.airlines import AirlineResponse


router = APIRouter()


# TODO: TEMPORARY MOCK DATA - Replace with database queries when Backend 2 is ready
MOCK_AIRLINES_DATA = [
    {
        "id": 1,
        "iata_code": "6E",
        "name": "IndiGo"
    },
    {
        "id": 2,
        "iata_code": "AI",
        "name": "Air India"
    },
    {
        "id": 3,
        "iata_code": "UK",
        "name": "Vistara"
    }
]


@router.get("/airlines", response_model=List[AirlineResponse])
async def get_airlines():
    """
    Get list of all airlines.
    
    Returns:
        List[AirlineResponse]: List of airline data including id, iata_code, and name.
    
    Note:
        Currently returns temporary mock data.
        Will be replaced with database queries once Backend 2 is ready.
    """
    # TODO: Replace with actual database query when Backend 2 is ready
    return MOCK_AIRLINES_DATA
