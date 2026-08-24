from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class ObservationResponse(BaseModel):
    id: int
    source: str
    airline: str
    flight_number: str | None = None
    origin: str
    destination: str
    travel_date: date
    departure_time: str | None = None
    stops: int
    fare: float
    currency: str
    collected_at: datetime


class RoutePriceIndex(BaseModel):
    origin: str
    destination: str
    travel_date: date
    latest_fare: float
    historical_average: float
    historical_min: float
    historical_max: float
    sample_count: int
    price_index: float = Field(..., description="Latest fare / historical average * 100")
    trend: str = Field(..., description="low, neutral, or high")


class FlightPriceIndex(BaseModel):
    source: str
    airline: str
    flight_number: str | None = None
    origin: str
    destination: str
    travel_date: date
    latest_fare: float
    historical_average: float
    historical_min: float
    historical_max: float
    sample_count: int
    price_index: float
    trend: str


class RouteHistoryResponse(BaseModel):
    route: str
    origin: str
    destination: str
    travel_date: date | None = None
    observations: list[ObservationResponse]
    index: RoutePriceIndex | None = None
