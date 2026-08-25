"""
Route schemas for API responses.
"""
from pydantic import BaseModel, Field


class RouteResponse(BaseModel):
    """Response schema for a flight route."""
    
    id: int = Field(..., description="Unique identifier for the route")
    origin: str = Field(..., description="Origin airport code (IATA)", min_length=3, max_length=3)
    destination: str = Field(..., description="Destination airport code (IATA)", min_length=3, max_length=3)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "origin": "DEL",
                    "destination": "BOM"
                }
            ]
        }
    }
