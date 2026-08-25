import asyncio
from datetime import date

import pytest

from backend.ingestion.sources.source_a import SourceA
from backend.ingestion.sources.source_b import SourceB
from backend.ingestion.sources.source_c import SourceC


@pytest.mark.asyncio
async def test_all_sources_return_one_record():
    collectors = [
        SourceA(),
        SourceB(),
        SourceC(),
    ]

    for collector in collectors:
        records = await collector.fetch(
            origin="DEL",
            destination="BOM",
            travel_date=date(2026, 9, 10),
        )

        assert len(records) == 1
        assert records[0]["origin"] == "DEL"
        assert records[0]["destination"] == "BOM"
        assert records[0]["currency"] in {"INR", "inr"}
