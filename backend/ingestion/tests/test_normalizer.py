from datetime import date, datetime, time, timezone

import pytest

from ingestion.normalizers.flight_normalizer import normalize_flight
from ingestion.schemas.flight_observation import FlightObservation
from ingestion.validators.observation_validator import validate_observation


@pytest.fixture
def raw_flight_record():
    return {
        "source": "source_a",
        "airline": "IndiGo",
        "flight_number": "6E-123",
        "origin": "del",
        "destination": "bom",
        "travel_date": "2026-09-10",
        "departure_time": "08:30:00",
        "stops": 0,
        "fare": "5482.00",
        "currency": "inr",
        "collected_at": "2026-08-24T12:00:00+00:00",
    }


def test_valid_raw_record(raw_flight_record):
    observation = normalize_flight(raw_flight_record)

    assert isinstance(observation, FlightObservation)
    assert observation.source == "source_a"
    assert observation.airline == "IndiGo"
    assert observation.flight_number == "6E-123"
    assert observation.origin == "DEL"
    assert observation.destination == "BOM"
    assert observation.travel_date == date(2026, 9, 10)
    assert observation.departure_time == time(8, 30)
    assert observation.stops == 0
    assert observation.fare == 5482.0
    assert observation.currency == "INR"
    assert observation.collected_at == datetime(2026, 8, 24, 12, 0, tzinfo=timezone.utc)


def test_lowercase_airport_codes_are_normalized(raw_flight_record):
    raw_flight_record["origin"] = "del"
    raw_flight_record["destination"] = "bom"

    observation = normalize_flight(raw_flight_record)

    assert observation.origin == "DEL"
    assert observation.destination == "BOM"


def test_lowercase_currency_is_normalized(raw_flight_record):
    raw_flight_record["currency"] = "inr"

    observation = normalize_flight(raw_flight_record)

    assert observation.currency == "INR"


def test_travel_date_string_is_converted_to_date(raw_flight_record):
    observation = normalize_flight(raw_flight_record)

    assert observation.travel_date == date(2026, 9, 10)


def test_departure_time_string_is_converted_to_time(raw_flight_record):
    observation = normalize_flight(raw_flight_record)

    assert observation.departure_time == time(8, 30)


def test_fare_string_is_converted_to_float(raw_flight_record):
    raw_flight_record["fare"] = "5482.00"

    observation = normalize_flight(raw_flight_record)

    assert observation.fare == 5482.0


def test_collected_at_iso_string_is_converted_to_timezone_aware_datetime(raw_flight_record):
    observation = normalize_flight(raw_flight_record)

    assert observation.collected_at.tzinfo is not None
    assert observation.collected_at.utcoffset() == timezone.utc.utcoffset(observation.collected_at)


def test_preserve_timezone_information(raw_flight_record):
    raw_flight_record["collected_at"] = "2026-08-24T12:00:00+02:00"

    observation = normalize_flight(raw_flight_record)

    assert observation.collected_at.tzinfo is not None
    assert observation.collected_at.utcoffset().total_seconds() == 7200


def test_preserve_source_provided_collected_at(raw_flight_record):
    collected_at = datetime(2026, 8, 24, 12, 0, tzinfo=timezone.utc)
    raw_flight_record["collected_at"] = collected_at

    observation = normalize_flight(raw_flight_record)

    assert observation.collected_at == collected_at


def test_optional_flight_number_is_preserved(raw_flight_record):
    observation = normalize_flight(raw_flight_record)

    assert observation.flight_number == "6E-123"


def test_optional_departure_time_is_preserved(raw_flight_record):
    raw_flight_record["departure_time"] = None

    observation = normalize_flight(raw_flight_record)

    assert observation.departure_time is None


def test_missing_required_field_raises_value_error(raw_flight_record):
    del raw_flight_record["fare"]

    with pytest.raises(ValueError, match="Missing required field: fare"):
        normalize_flight(raw_flight_record)


def test_invalid_fare_raises_value_error(raw_flight_record):
    raw_flight_record["fare"] = "not-a-number"

    with pytest.raises(ValueError, match="Invalid fare"):
        normalize_flight(raw_flight_record)


def test_invalid_date_raises_value_error(raw_flight_record):
    raw_flight_record["travel_date"] = "2026-99-99"

    with pytest.raises(ValueError, match="Invalid travel_date"):
        normalize_flight(raw_flight_record)


def test_invalid_time_raises_value_error(raw_flight_record):
    raw_flight_record["departure_time"] = "not-a-time"

    with pytest.raises(ValueError, match="Invalid departure_time"):
        normalize_flight(raw_flight_record)


def test_invalid_collected_at_raises_value_error(raw_flight_record):
    raw_flight_record["collected_at"] = "not-a-timestamp"

    with pytest.raises(ValueError, match="Invalid collected_at"):
        normalize_flight(raw_flight_record)


def test_invalid_route_is_rejected_by_validation_layer(raw_flight_record):
    raw_flight_record["origin"] = "BOM"
    raw_flight_record["destination"] = "BOM"

    with pytest.raises(ValueError, match="Origin and destination cannot be the same"):
        validate_observation(normalize_flight(raw_flight_record))
