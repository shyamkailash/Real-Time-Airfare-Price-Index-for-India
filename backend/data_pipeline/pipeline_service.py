from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.database.repositories.collection_run_repository import (
    complete_collection_run,
    create_collection_run,
)
from backend.database.repositories.fare_observation_repository import (
    create_fare_observation,
)


def run_fare_collection(
    db: Session,
    *,
    source: str,
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    started_at = datetime.now(timezone.utc)

    run = create_collection_run(
        db,
        source=source,
        started_at=started_at,
        status="running",
    )

    records_collected = len(observations)
    records_inserted = 0
    records_rejected = 0

    try:
        for observation in observations:
            try:
                with db.begin_nested():
                    create_fare_observation(
                        db,
                        source=source,
                        airline_id=observation["airline_id"],
                        route_id=observation["route_id"],
                        flight_number=observation.get("flight_number"),
                        travel_date=observation["travel_date"],
                        departure_time=observation["departure_time"],
                        stops=observation["stops"],
                        fare=Decimal(str(observation["fare"])),
                        currency=observation["currency"],
                        collected_at=observation.get(
                            "collected_at",
                            datetime.now(timezone.utc),
                        ),
                    )

                records_inserted += 1

            except IntegrityError:
                records_rejected += 1

        complete_collection_run(
            db,
            run,
            status="completed",
            records_collected=records_collected,
            records_inserted=records_inserted,
            records_rejected=records_rejected,
            completed_at=datetime.now(timezone.utc),
        )

        db.commit()

        return {
            "run_id": run.id,
            "status": run.status,
            "records_collected": records_collected,
            "records_inserted": records_inserted,
            "records_rejected": records_rejected,
        }

    except Exception:
        db.rollback()
        raise