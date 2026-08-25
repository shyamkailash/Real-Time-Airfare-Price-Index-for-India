from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health
from api.routes import routes
from api.routes import airlines
from api.routes import fares
from backend.api.routes.airfare import router as airfare_router

from backend.database.session import initialize_database
from backend.storage.database import create_database


# Initialize database
create_database()
initialize_database()


# Create FastAPI application
app = FastAPI(
    title="Real-Time Airfare Price Index for India",
    version="1.0.0",
    description="Historical airfare collection, validation, deduplication, and price index API.",
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Existing API routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(routes.router, prefix="/api", tags=["routes"])
app.include_router(airlines.router, prefix="/api", tags=["airlines"])
app.include_router(fares.router, prefix="/api", tags=["fares"])

# New integrated airfare router
app.include_router(airfare_router)