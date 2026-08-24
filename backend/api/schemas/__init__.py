"""
API Schemas Package
Contains Pydantic models for request/response validation
"""
from api.schemas.health import HealthResponse
from api.schemas.routes import RouteResponse

__all__ = ["HealthResponse", "RouteResponse"]
