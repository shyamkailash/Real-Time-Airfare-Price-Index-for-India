from datetime import date, time
from typing import Any

from backend.data_pipeline.collectors.base import FareCollector


class MockFareCollector(FareCollector):
    """Mock fare collector for development and testing."""

    def collect(self) -> list[dict[str, Any]]:
        return [
            {
                "airline_id": 1,
                "route_id": 1,
                "flight_number": "6E501",
                "travel_date": date(2026, 9, 15),
                "departure_time": time(8, 30),
                "stops": 0,
                "fare": "5200.00",
                "currency": "INR",
            },
            {
                "airline_id": 1,
                "route_id": 1,
                "flight_number": "6E502",
                "travel_date": date(2026, 9, 15),
                "departure_time": time(11, 0),
                "stops": 0,
                "fare": "6100.00",
                "currency": "INR",
            },
        ]