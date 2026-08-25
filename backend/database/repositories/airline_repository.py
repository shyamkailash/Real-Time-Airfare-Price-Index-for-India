from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models.airline import Airline


def get_all_airlines(db: Session) -> list[Airline]:
    result = db.execute(
        select(Airline).order_by(Airline.id)
    )
    return list(result.scalars().all())


def get_airline_by_id(
    db: Session,
    airline_id: int,
) -> Airline | None:
    return db.get(Airline, airline_id)