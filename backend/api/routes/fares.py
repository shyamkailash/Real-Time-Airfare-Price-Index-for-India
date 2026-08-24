"""
Fares API routes.
Provides endpoints for airfare observation data.
"""
from fastapi import APIRouter
from typing import List

from api.schemas.fares import FareResponse


router = APIRouter()


# TODO: TEMPORARY MOCK DATA - Replace with database queries when Backend 2 is ready
MOCK_FARES_DATA = [
    {
        "id": 1,
        "source": "example_source",
        "airline": "IndiGo",
        "origin": "DEL",
        "destination": "BOM",
        "travel_date": "2026-09-10",
        "departure_time": "08:30:00",
        "stops": 0,
        "fare": 5482.00,
        "currency": "INR",
        "collected_at": "2026-08-24T12:00:00Z"
    },
    {
        "id": 2,
        "source": "example_source",
        "airline": "Air India",
        "origin": "BOM",
        "destination": "BLR",
        "travel_date": "2026-09-15",
        "departure_time": "14:45:00",
        "stops": 1,
        "fare": 6320.50,
        "currency": "INR",
        "collected_at": "2026-08-24T12:05:00Z"
    },
    {
        "id": 3,
        "source": "example_source",
        "airline": "Vistara",
        "origin": "BLR",
        "destination": "DEL",
        "travel_date": "2026-09-20",
        "departure_time": "18:15:00",
        "stops": 0,
        "fare": 7845.75,
        "currency": "INR",
        "collected_at": "2026-08-24T12:10:00Z"
    },
    {
        "id": 4,
        "source": "example_source",
        "airline": "IndiGo",
        "origin": "DEL",
        "destination": "CCU",
        "travel_date": "2026-09-12",
        "departure_time": "06:00:00",
        "stops": 0,
        "fare": 4299.00,
        "currency": "INR",
        "collected_at": "2026-08-24T12:15:00Z"
    }
]


@router.get("/fares", response_model=List[FareResponse])
async def get_fares():
    """
    Get list of all fare observations.
    
    Returns:
        List[FareResponse]: List of standardized airfare observations including
                           airline, route, price, travel date, and collection metadata.
    
    Note:
        Currently returns temporary mock data.
        Will be replaced with database queries once Backend 2 is ready.
    """
    # TODO: Replace with actual database query when Backend 2 is ready
    return MOCK_FARES_DATA
