from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models.fare_observation import FareObservation

def create_fare_observation(
    db: Session,
    *,
    source: str,
    airline_id: int,
    route_id: int,
    travel_date: date,
    departure_time: time,
    stops: int,
    fare: Decimal,
    currency: str,
    collected_at: datetime,
    flight_number: str | None = None,
) -> FareObservation:
    observation = FareObservation(
        source=source,
        airline_id=airline_id,
        route_id=route_id,
        flight_number=flight_number,
        travel_date=travel_date,
        departure_time=departure_time,
        stops=stops,
        fare=fare,
        currency=currency,
        collected_at=collected_at,
    )

    db.add(observation)
    db.flush()

    return observation

def get_fare_observation_by_id(
    db: Session,
    observation_id: int,
) -> FareObservation | None:
    return db.get(FareObservation, observation_id)


def get_fare_observations(
    db: Session,
    *,
    travel_date: date | None = None,
    airline_id: int | None = None,
    route_id: int | None = None,
) -> list[FareObservation]:
    stmt = select(FareObservation)

    if travel_date is not None:
        stmt = stmt.where(
            FareObservation.travel_date == travel_date
        )

    if airline_id is not None:
        stmt = stmt.where(
            FareObservation.airline_id == airline_id
        )

    if route_id is not None:
        stmt = stmt.where(
            FareObservation.route_id == route_id
        )

    stmt = stmt.order_by(FareObservation.id)

    result = db.execute(stmt)
    return list(result.scalars().all())