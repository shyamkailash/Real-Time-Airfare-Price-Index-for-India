"""
Routes API endpoints.
"""
from fastapi import APIRouter
from typing import List

from api.schemas.routes import RouteResponse

router = APIRouter()


# ===========================
# TEMPORARY MOCK DATA
# TODO: Replace with Backend 2 repository/service when database is ready
# ===========================
MOCK_ROUTES = [
    {"id": 1, "origin": "DEL", "destination": "BOM"},
    {"id": 2, "origin": "MAA", "destination": "DEL"},
    {"id": 3, "origin": "BOM", "destination": "MAA"},
    {"id": 4, "origin": "BLR", "destination": "DEL"},
    {"id": 5, "origin": "DEL", "destination": "BLR"},
    {"id": 6, "origin": "CCU", "destination": "BOM"},
]


@router.get(
    "/routes",
    response_model=List[RouteResponse],
    summary="Get all flight routes",
    description="Returns a list of available flight routes. Currently using mock data until Backend 2 database is ready.",
    tags=["routes"]
)
async def get_routes() -> List[RouteResponse]:
    """
    Retrieve all available flight routes.
    
    Returns:
        List[RouteResponse]: List of flight routes with origin and destination.
    
    Note:
        This endpoint currently returns mock data. It will be connected to
        the Backend 2 repository/service once the PostgreSQL database is ready.
    """
    # TODO: Replace with actual repository call
    # Example: routes = await route_repository.get_all_routes()
    return [RouteResponse(**route) for route in MOCK_ROUTES]
