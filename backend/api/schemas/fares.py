"""
Pydantic schemas for fares API endpoints.
"""
from pydantic import BaseModel
from datetime import date, time, datetime


class FareResponse(BaseModel):
    """
    Response schema for fare observation data.
    """
    id: int
    source: str
    airline: str
    origin: str
    destination: str
    travel_date: date
    departure_time: time
    stops: int
    fare: float
    currency: str
    collected_at: datetime
