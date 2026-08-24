import asyncio
from datetime import date

from ingestion.sources.source_a import SourceA
from ingestion.collectors.flight_collector import FlightCollector


async def main():
    source = SourceA()
    collector = FlightCollector(source)

    results = await collector.collect(
        origin="DEL",
        destination="BOM",
        travel_date=date(2026, 9, 10)
    )

    for flight in results:
        print(flight.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())