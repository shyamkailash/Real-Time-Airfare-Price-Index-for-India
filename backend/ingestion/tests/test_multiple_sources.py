import asyncio
from datetime import date

from ingestion.sources.source_a import SourceA
from ingestion.sources.source_b import SourceB
from ingestion.sources.source_c import SourceC


async def main():
    collectors = [
        SourceA(),
        SourceB(),
        SourceC(),
    ]

    for collector in collectors:
        print("\n" + "=" * 60)
        print(f"COLLECTOR: {collector.__class__.__name__}")
        print("=" * 60)

        records = await collector.fetch(
            origin="DEL",
            destination="BOM",
            travel_date=date(2026, 9, 10),
        )

        for record in records:
            print(record)


if __name__ == "__main__":
    asyncio.run(main())