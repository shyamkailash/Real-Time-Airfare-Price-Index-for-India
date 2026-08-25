from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database.models.collection_run import CollectionRun

def create_collection_run(
    db: Session,
    *,
    source: str,
    started_at: datetime,
    status: str,
    records_collected: int = 0,
    records_inserted: int = 0,
    records_rejected: int = 0,
) -> CollectionRun:
    run = CollectionRun(
        source=source,
        started_at=started_at,
        status=status,
        records_collected=records_collected,
        records_inserted=records_inserted,
        records_rejected=records_rejected,
    )

    db.add(run)
    db.flush()

    return run

def complete_collection_run(
    db: Session,
    run: CollectionRun,
    *,
    status: str,
    records_collected: int,
    records_inserted: int,
    records_rejected: int,
    completed_at: datetime,
    error_message: str | None = None,
) -> CollectionRun:
    run.status = status
    run.records_collected = records_collected
    run.records_inserted = records_inserted
    run.records_rejected = records_rejected
    run.completed_at = completed_at
    run.error_message = error_message

    db.flush()

    return run

def update_collection_run(
    db: Session,
    run: CollectionRun,
    *,
    status: str | None = None,
    records_collected: int | None = None,
    records_inserted: int | None = None,
    records_rejected: int | None = None,
    completed_at: datetime | None = None,
    error_message: str | None = None,
) -> CollectionRun:
    if status is not None:
        run.status = status

    if records_collected is not None:
        run.records_collected = records_collected

    if records_inserted is not None:
        run.records_inserted = records_inserted

    if records_rejected is not None:
        run.records_rejected = records_rejected

    if completed_at is not None:
        run.completed_at = completed_at

    if error_message is not None:
        run.error_message = error_message

    db.flush()

    return run

def get_collection_run_by_id(
    db: Session,
    run_id: int,
) -> CollectionRun | None:
    return db.get(CollectionRun, run_id)


def get_collection_runs(
    db: Session,
) -> list[CollectionRun]:
    result = db.execute(
        select(CollectionRun).order_by(CollectionRun.id.desc())
    )
    return list(result.scalars().all())