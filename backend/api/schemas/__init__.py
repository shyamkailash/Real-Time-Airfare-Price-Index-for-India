"""
API Schemas Package
Contains Pydantic models for request/response validation
"""
from backend.api.schemas.health import HealthResponse
from backend.api.schemas.routes import RouteResponse

__all__ = ["HealthResponse", "RouteResponse"]
