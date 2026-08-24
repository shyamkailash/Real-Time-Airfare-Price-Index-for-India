"""
FastAPI Application Entry Point
Backend Member 3 - FastAPI & Integration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health
from api.routes import routes
from api.routes import airlines
from api.routes import fares

# Create FastAPI application
app = FastAPI(
    title="Airfare Price Index API",
    description="Real-Time Airfare Price Index for India",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(routes.router, prefix="/api", tags=["routes"])
app.include_router(airlines.router, prefix="/api", tags=["airlines"])
app.include_router(fares.router, prefix="/api", tags=["fares"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
