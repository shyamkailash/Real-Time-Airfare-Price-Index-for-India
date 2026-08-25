import asyncio
from datetime import date

import pytest

from ingestion.collectors.flight_collector import FlightCollector
from ingestion.sources.source_a import SourceA


@pytest.mark.asyncio
async def test_source_a_collector_returns_valid_observation():
    source = SourceA()
    collector = FlightCollector(source)

    results = await collector.collect(
        origin="DEL",
        destination="BOM",
        travel_date=date(2026, 9, 10),
    )

    assert len(results) == 1
    assert results[0].source == "source_a"
    assert results[0].origin == "DEL"
    assert results[0].destination == "BOM"
    assert results[0].fare > 0
