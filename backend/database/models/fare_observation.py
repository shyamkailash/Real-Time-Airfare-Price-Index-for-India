from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.connection import Base


class FareObservation(Base):
    __tablename__ = "fare_observations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    airline_id: Mapped[int] = mapped_column(
        ForeignKey("airline.id"),
        nullable=False,
    )

    route_id: Mapped[int] = mapped_column(
        ForeignKey("routes.id"),
        nullable=False,
    )

    flight_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    travel_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    departure_time: Mapped[time] = mapped_column(
        Time(timezone=True),
        nullable=False,
    )

    stops: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    fare: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    __table_args__ = (
        CheckConstraint(
            "fare > 0",
            name="fare_observations_fare_positive",
        ),
        CheckConstraint(
            "stops >= 0",
            name="fare_observations_stops_nonnegative",
        ),
        CheckConstraint(
            "currency = 'INR'",
            name="fare_observations_currency_inr",
        ),
        UniqueConstraint(
            "source",
            "airline_id",
            "route_id",
            "travel_date",
            "departure_time",
            name="fare_observations_unique_observation",
        ),
        Index(
            "fki_fare_observations_airline_fkey",
            "airline_id",
        ),
        Index(
            "fki_fare_observations_route_fkey",
            "route_id",
        ),
        Index(
            "idx_fare_observations_airline_id",
            "airline_id",
        ),
        Index(
            "idx_fare_observations_route_id",
            "route_id",
        ),
        Index(
            "idx_fare_observations_travel_date",
            "travel_date",
        ),
    )