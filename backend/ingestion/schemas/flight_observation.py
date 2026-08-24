from datetime import date, datetime, time

from pydantic import BaseModel, Field, field_validator


class FlightObservation(BaseModel):
    source: str = Field(..., min_length=1)
    airline: str = Field(..., min_length=1)
    flight_number: str | None = Field(
        default=None,
        min_length=2,
        max_length=20,
    )
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)

    travel_date: date
    departure_time: time | None = None

    stops: int = Field(..., ge=0)
    fare: float = Field(..., gt=0)

    currency: str = Field(..., min_length=3, max_length=3)

    collected_at: datetime

    @field_validator("origin", "destination", "currency")
    @classmethod
    def normalize_codes(cls, value: str) -> str:
        return value.upper()