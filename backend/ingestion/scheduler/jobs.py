from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

from ingestion.collectors.flight_collector import FlightCollector
from ingestion.schemas.collection_summary import CollectionSummary
from ingestion.sources.source_a import SourceA
from ingestion.sources.source_b import SourceB
from ingestion.sources.source_c import SourceC
from ingestion.utils.logging import setup_logger
from storage.database import DATABASE_PATH, SessionLocal, create_database
from storage.repository import FlightObservationRepository


logger = setup_logger(__name__)


async def collect_and_store(
    origin: str,
    destination: str,
    travel_date: date,
):
    """
    Collect flight observations from all configured sources,
    filter out exact duplicates, and save only new records.
    """
    started_at = datetime.now(timezone.utc)
    sources = [
        SourceA(),
        SourceB(),
        SourceC(),
    ]
    total_sources = len(sources)
    successful_sources = 0
    failed_sources = 0
    all_observations = []

    create_database()

    for source in sources:
        collector = FlightCollector(source)

        try:
            observations = await collector.collect(
                origin=origin,
                destination=destination,
                travel_date=travel_date,
            )
        except Exception:
            failed_sources += 1
            logger.exception(
                "Failed to collect observations from %s",
                source.__class__.__name__,
            )
            continue

        successful_sources += 1
        all_observations.extend(observations)

    total_collected = len(all_observations)

    if not all_observations:
        summary = CollectionSummary(
            total_sources=total_sources,
            successful_sources=successful_sources,
            failed_sources=failed_sources,
            total_collected=0,
            duplicates_skipped=0,
            new_records_stored=0,
            started_at=started_at,
            completed_at=datetime.now(timezone.utc),
        )
        collect_and_store.last_summary = summary
        logger.info(
            "No flight observations collected from any source. "
            "Successful sources: %s; Failed sources: %s",
            successful_sources,
            failed_sources,
        )
        return []

    with SessionLocal() as session:
        repository = FlightObservationRepository(session)
        saved_records = repository.save_many_if_new(all_observations)

    duplicates_skipped = total_collected - len(saved_records)
    summary = CollectionSummary(
        total_sources=total_sources,
        successful_sources=successful_sources,
        failed_sources=failed_sources,
        total_collected=total_collected,
        duplicates_skipped=duplicates_skipped,
        new_records_stored=len(saved_records),
        started_at=started_at,
        completed_at=datetime.now(timezone.utc),
    )
    collect_and_store.last_summary = summary

    logger.info(
        "Collection summary: collected=%s, duplicates_skipped=%s, new_records=%s",
        total_collected,
        duplicates_skipped,
        len(saved_records),
    )

    return saved_records


collect_and_store.last_summary = None


if __name__ == "__main__":
    import asyncio

    async def main():
        if DATABASE_PATH.exists():
            DATABASE_PATH.unlink()

        print("\n" + "=" * 60)
        print("PHASE 2 SCHEDULER TEST")
        print("=" * 60)
        print("Sources configured: 3")

        records = await collect_and_store(
            origin="DEL",
            destination="BOM",
            travel_date=date(2026, 9, 10),
        )

        print(f"Total observations collected: {collect_and_store.last_summary.total_collected}")
        print(f"Duplicates skipped: {collect_and_store.last_summary.duplicates_skipped}")
        print(f"New records stored: {collect_and_store.last_summary.new_records_stored}")

        print("\n" + "=" * 60)
        print("RUNNING SECOND COLLECTION")
        print("=" * 60)

        second_records = await collect_and_store(
            origin="DEL",
            destination="BOM",
            travel_date=date(2026, 9, 10),
        )

        print(f"Total observations collected: {collect_and_store.last_summary.total_collected}")
        print(f"Duplicates skipped: {collect_and_store.last_summary.duplicates_skipped}")
        print(f"New records stored: {collect_and_store.last_summary.new_records_stored}")

        print("\n" + "=" * 60)
        print("PHASE 2 TEST COMPLETED SUCCESSFULLY")
        print("=" * 60)

        print(f"First run records: {len(records)}")
        print(f"Second run records: {len(second_records)}")

    asyncio.run(main())