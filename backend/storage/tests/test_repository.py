import asyncio
from datetime import date

from ingestion.collectors.flight_collector import FlightCollector
from ingestion.sources.source_a import SourceA
from ingestion.sources.source_b import SourceB
from ingestion.sources.source_c import SourceC

from storage.database import SessionLocal, create_database
from storage.repository import FlightObservationRepository


async def collect_from_all_sources():
    travel_date = date(2026, 9, 10)

    sources = [
        SourceA(),
        SourceB(),
        SourceC(),
    ]

    all_observations = []

    for source in sources:
        collector = FlightCollector(source)

        observations = await collector.collect(
            origin="DEL",
            destination="BOM",
            travel_date=travel_date,
        )

        all_observations.extend(observations)

    return all_observations


def main():
    create_database()

    observations = asyncio.run(
        collect_from_all_sources()
    )

    session = SessionLocal()

    try:
        repository = FlightObservationRepository(session)

        records = repository.save_many(observations)

        print("\n" + "=" * 60)
        print("DATABASE MULTI-SOURCE INSERT TEST")
        print("=" * 60)

        print(f"Total observations saved: {len(records)}")

        for record in records:
            print(
                {
                    "id": record.id,
                    "source": record.source,
                    "airline": record.airline,
                    "origin": record.origin,
                    "destination": record.destination,
                    "travel_date": str(record.travel_date),
                    "fare": record.fare,
                    "currency": record.currency,
                }
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()