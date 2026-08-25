from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models.airport import Airport


def get_all_airports(db: Session) -> list[Airport]:
    result = db.execute(
        select(Airport).order_by(Airport.id)
    )
    return list(result.scalars().all())


def get_airport_by_id(
    db: Session,
    airport_id: int,
) -> Airport | None:
    return db.get(Airport, airport_id)


def get_airport_by_iata(
    db: Session,
    iata_code: str,
) -> Airport | None:
    result = db.execute(
        select(Airport).where(Airport.iata_code == iata_code)
    )
    return result.scalar_one_or_none()