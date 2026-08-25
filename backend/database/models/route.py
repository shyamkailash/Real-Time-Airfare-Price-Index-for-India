from sqlalchemy import CheckConstraint, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.connection import Base


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    origin_airport_id: Mapped[int] = mapped_column(
        ForeignKey("airports.id"),
        nullable=False,
    )

    destination_airport_id: Mapped[int] = mapped_column(
        ForeignKey("airports.id"),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "origin_airport_id <> destination_airport_id",
            name="routes_origin_destination_different",
        ),
        UniqueConstraint(
            "origin_airport_id",
            "destination_airport_id",
            name="routes_origin_destination_unique",
        ),
        Index(
            "fki_routes_origin_airport_fkey",
            "origin_airport_id",
        ),
        Index(
            "fki_routes_destination_airport_fkey",
            "destination_airport_id",
        ),
    )