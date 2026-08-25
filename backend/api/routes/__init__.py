"""
API Routes Package
Contains all FastAPI route handlers
"""
from backend.api.routes.health import router as health_router
from backend.api.routes.routes import router as routes_router
from .airfare import router as airfare_router

__all__ = ["health_router", "routes_router", "airfare_router"]
