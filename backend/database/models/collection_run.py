from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.connection import Base


class CollectionRun(Base):
    __tablename__ = "collection_runs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        "started_id",
        DateTime(timezone=True),
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    records_collected: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    records_inserted: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    records_rejected: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )