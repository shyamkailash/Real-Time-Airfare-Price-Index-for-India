from __future__ import annotations

from datetime import date, datetime, timezone

from fastapi.testclient import TestClient

from backend.main import app
from backend.storage.database import SessionLocal
from backend.storage.models import FlightObservationModel


client = TestClient(app)


def seed_route_data():
    with SessionLocal() as session:
        session.query(FlightObservationModel).delete()
        session.add_all([
            FlightObservationModel(
                source="source_a",
                airline="IndiGo",
                flight_number="6E-123",
                origin="DEL",
                destination="BOM",
                travel_date=date(2026, 9, 10),
                departure_time=datetime.strptime("08:30:00", "%H:%M:%S").time(),
                stops=0,
                fare=5482.0,
                currency="INR",
                collected_at=datetime(2026, 9, 1, 8, 30, tzinfo=timezone.utc),
            ),
            FlightObservationModel(
                source="source_b",
                airline="Air India",
                flight_number="AI-456",
                origin="DEL",
                destination="BOM",
                travel_date=date(2026, 9, 10),
                departure_time=datetime.strptime("10:15:00", "%H:%M:%S").time(),
                stops=0,
                fare=6200.0,
                currency="INR",
                collected_at=datetime(2026, 9, 1, 10, 15, tzinfo=timezone.utc),
            ),
        ])
        session.commit()


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_route_history_endpoint_returns_index():
    seed_route_data()
    response = client.get("/api/routes/DEL/BOM/2026-09-10")
    assert response.status_code == 200
    payload = response.json()
    assert payload["origin"] == "DEL"
    assert payload["destination"] == "BOM"
    assert payload["index"]["sample_count"] == 2
    assert payload["index"]["latest_fare"] == 6200.0


def test_flight_history_endpoint_returns_flight_index():
    seed_route_data()
    response = client.get(
        "/api/flights/history",
        params={
            "source": "source_a",
            "flight_number": "6E-123",
            "origin": "DEL",
            "destination": "BOM",
            "travel_date": "2026-09-10",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["flight_number"] == "6E-123"
    assert payload[0]["price_index"] > 0
