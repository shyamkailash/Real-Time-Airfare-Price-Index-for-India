from typing import Any

from sqlalchemy.orm import Session

from backend.data_pipeline.collectors.base import FareCollector
from backend.data_pipeline.pipeline_service import run_fare_collection


def run_collector(
    db: Session,
    collector: FareCollector,
    *,
    source: str,
) -> dict[str, Any]:
    observations = collector.collect()

    return run_fare_collection(
        db,
        source=source,
        observations=observations,
    )