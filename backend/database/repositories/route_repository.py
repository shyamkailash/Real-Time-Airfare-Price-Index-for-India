from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models.route import Route


def get_all_routes(db: Session) -> list[Route]:
    result = db.execute(
        select(Route).order_by(Route.id)
    )
    return list(result.scalars().all())


def get_route_by_id(
    db: Session,
    route_id: int,
) -> Route | None:
    return db.get(Route, route_id)


def get_route(
    db: Session,
    origin_airport_id: int,
    destination_airport_id: int,
) -> Route | None:
    result = db.execute(
        select(Route).where(
            Route.origin_airport_id == origin_airport_id,
            Route.destination_airport_id == destination_airport_id,
        )
    )
    return result.scalar_one_or_none()