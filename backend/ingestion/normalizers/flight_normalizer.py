from __future__ import annotations

import math
from collections.abc import Mapping
from datetime import date, datetime, time
from typing import Any

from ingestion.schemas.flight_observation import FlightObservation


REQUIRED_FIELDS = (
    "source",
    "airline",
    "origin",
    "destination",
    "travel_date",
    "stops",
    "fare",
    "currency",
    "collected_at",
)


def _require_field(raw_flight: Mapping[str, Any], field_name: str) -> Any:
    if field_name not in raw_flight or raw_flight[field_name] is None:
        raise ValueError(f"Missing required field: {field_name}")
    return raw_flight[field_name]


def _parse_travel_date(raw_value: Any) -> date:
    if isinstance(raw_value, datetime):
        return raw_value.date()
    if isinstance(raw_value, date):
        return raw_value

    try:
        return date.fromisoformat(str(raw_value))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid travel_date: {raw_value!r}") from exc


def _parse_departure_time(raw_value: Any) -> time | None:
    if raw_value is None:
        return None

    if isinstance(raw_value, time):
        return raw_value

    try:
        return time.fromisoformat(str(raw_value))
    except ValueError as exc:
        raise ValueError(f"Invalid departure_time: {raw_value!r}") from exc


def _parse_stops(raw_value: Any) -> int:
    if raw_value is None:
        raise ValueError("Missing required field: stops")

    if isinstance(raw_value, bool):
        raise ValueError(f"Invalid stops: {raw_value!r}")

    try:
        return int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid stops: {raw_value!r}") from exc


def _parse_fare(raw_value: Any) -> float:
    if raw_value is None:
        raise ValueError("Missing required field: fare")

    if isinstance(raw_value, bool):
        raise ValueError(f"Invalid fare: {raw_value!r}")

    try:
        fare = float(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid fare: {raw_value!r}") from exc

    if not math.isfinite(fare):
        raise ValueError(f"Invalid fare: {raw_value!r}")

    return fare


def _parse_collected_at(raw_value: Any) -> datetime:
    if raw_value is None:
        raise ValueError("Missing required field: collected_at")

    if isinstance(raw_value, datetime):
        if raw_value.tzinfo is None or raw_value.utcoffset() is None:
            raise ValueError(f"Invalid collected_at: {raw_value!r}")
        return raw_value

    try:
        normalized = str(raw_value).strip()
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"
        parsed = datetime.fromisoformat(normalized)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid collected_at: {raw_value!r}") from exc

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"Invalid collected_at: {raw_value!r}")

    return parsed


def normalize_flight(raw_flight: Mapping[str, Any]) -> FlightObservation:
    """Convert a heterogeneous source record into a canonical FlightObservation."""
    if not isinstance(raw_flight, Mapping):
        raise ValueError("Raw flight payload must be a mapping of key/value pairs.")

    for field_name in REQUIRED_FIELDS:
        _require_field(raw_flight, field_name)

    source = str(raw_flight["source"]).strip()
    airline = str(raw_flight["airline"]).strip()
    flight_number = raw_flight.get("flight_number")
    if flight_number is not None:
        flight_number = str(flight_number).strip() or None

    origin = str(raw_flight["origin"]).strip().upper()
    destination = str(raw_flight["destination"]).strip().upper()
    travel_date = _parse_travel_date(raw_flight["travel_date"])
    departure_time = _parse_departure_time(raw_flight.get("departure_time"))
    stops = _parse_stops(raw_flight["stops"])
    fare = _parse_fare(raw_flight["fare"])
    currency = str(raw_flight["currency"]).strip().upper()
    collected_at = _parse_collected_at(raw_flight["collected_at"])

    observation = FlightObservation(
        source=source,
        airline=airline,
        flight_number=flight_number,
        origin=origin,
        destination=destination,
        travel_date=travel_date,
        departure_time=departure_time,
        stops=stops,
        fare=fare,
        currency=currency,
        collected_at=collected_at,
    )

    return observation


__all__ = ["normalize_flight"]
