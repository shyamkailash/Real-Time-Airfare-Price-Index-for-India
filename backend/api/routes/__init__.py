"""
API Routes Package
Contains all FastAPI route handlers
"""
from api.routes.health import router as health_router
from api.routes.routes import router as routes_router

__all__ = ["health_router", "routes_router"]
