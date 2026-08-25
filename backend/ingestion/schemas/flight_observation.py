from datetime import date, datetime, time

from pydantic import BaseModel, Field, field_validator, model_validator


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
        normalized = value.upper()
        if len(normalized) != 3 or not normalized.isalpha():
            raise ValueError("Airport and currency codes must be 3 alphabetic characters.")
        return normalized

    @field_validator("collected_at")
    @classmethod
    def validate_collected_at_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("collected_at must be timezone-aware.")
        return value

    @model_validator(mode="after")
    def validate_route_and_departure(self):
        if self.origin == self.destination:
            raise ValueError("Origin and destination cannot be the same.")
        if self.departure_time is not None:
            self.departure_time.isoformat()
        return self