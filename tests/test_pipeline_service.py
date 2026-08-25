from datetime import date, time
from uuid import uuid4

from backend.data_pipeline.pipeline_service import run_fare_collection
from backend.database.repositories.fare_observation_repository import (
    get_fare_observations,
)


def unique_source(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


def test_pipeline_inserts_valid_observation(db):
    source = unique_source("pytest_valid")

    result = run_fare_collection(
        db,
        source=source,
        observations=[
            {
                "airline_id": 1,
                "route_id": 1,
                "flight_number": "6E901",
                "travel_date": date(2026, 10, 1),
                "departure_time": time(9, 0),
                "stops": 0,
                "fare": "6500.00",
                "currency": "INR",
            }
        ],
    )

    assert result["status"] == "completed"
    assert result["records_collected"] == 1
    assert result["records_inserted"] == 1
    assert result["records_rejected"] == 0

    observations = get_fare_observations(db)

    assert any(
        observation.source == source
        and observation.flight_number == "6E901"
        for observation in observations
    )


def test_pipeline_rejects_invalid_fare(db):
    source = unique_source("pytest_invalid")

    result = run_fare_collection(
        db,
        source=source,
        observations=[
            {
                "airline_id": 1,
                "route_id": 1,
                "flight_number": "6E902",
                "travel_date": date(2026, 10, 2),
                "departure_time": time(10, 0),
                "stops": 0,
                "fare": "-500.00",
                "currency": "INR",
            }
        ],
    )

    assert result["status"] == "completed"
    assert result["records_collected"] == 1
    assert result["records_inserted"] == 0
    assert result["records_rejected"] == 1


def test_pipeline_rejects_duplicate(db):
    source = unique_source("pytest_duplicate")

    observation = {
        "airline_id": 1,
        "route_id": 1,
        "flight_number": "6E903",
        "travel_date": date(2026, 10, 3),
        "departure_time": time(11, 0),
        "stops": 0,
        "fare": "7000.00",
        "currency": "INR",
    }

    first_result = run_fare_collection(
        db,
        source=source,
        observations=[observation],
    )

    second_result = run_fare_collection(
        db,
        source=source,
        observations=[observation],
    )

    assert first_result["records_inserted"] == 1
    assert first_result["records_rejected"] == 0

    assert second_result["records_inserted"] == 0
    assert second_result["records_rejected"] == 1