from datetime import date, time
from uuid import uuid4

from backend.data_pipeline.collectors.base import FareCollector
from backend.data_pipeline.pipeline_runner import run_collector


class TestCollector(FareCollector):
    def collect(self):
        return [
            {
                "airline_id": 1,
                "route_id": 1,
                "flight_number": "TEST001",
                "travel_date": date(2026, 11, 1),
                "departure_time": time(8, 0),
                "stops": 0,
                "fare": "5000.00",
                "currency": "INR",
            }
        ]


def test_run_collector(db):
    source = f"pytest_runner_{uuid4().hex[:8]}"

    result = run_collector(
        db,
        TestCollector(),
        source=source,
    )

    assert result["status"] == "completed"
    assert result["records_collected"] == 1
    assert result["records_inserted"] == 1
    assert result["records_rejected"] == 0