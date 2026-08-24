from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, Float, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from storage.database import Base


class FlightObservationModel(Base):
    __tablename__ = "flight_observations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    airline: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    flight_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True,
    )

    origin: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        index=True,
    )

    destination: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        index=True,
    )

    travel_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    departure_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    stops: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    fare: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )