from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import backend.ingestion.scheduler.jobs as scheduler_module
from backend.ingestion.schemas.flight_observation import FlightObservation
from backend.storage.database import Base
from backend.storage.models import FlightObservationModel
from backend.storage.repository import FlightObservationRepository


def make_session_factory(tmp_path):
    db_path = tmp_path / "phase2_test.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def make_observation(**overrides):
    base = {
        "source": "source_a",
        "airline": "IndiGo",
        "flight_number": "6E-123",
        "origin": "DEL",
        "destination": "BOM",
        "travel_date": date(2026, 9, 10),
        "departure_time": datetime.strptime("08:30:00", "%H:%M:%S").time(),
        "stops": 0,
        "fare": 5482.0,
        "currency": "INR",
        "collected_at": datetime(2026, 9, 1, 8, 30, tzinfo=timezone.utc),
    }
    base.update(overrides)
    return FlightObservation(**base)


def test_repository_exact_duplicate_detection(tmp_path):
    session_factory = make_session_factory(tmp_path)
    with session_factory() as session:
        repository = FlightObservationRepository(session)
        observation = make_observation()

        saved = repository.save_if_new(observation)
        duplicate = repository.save_if_new(observation)

        assert saved is not None
        assert duplicate is None

        rows = session.scalars(select(FlightObservationModel)).all()
        assert len(rows) == 1


def test_repository_price_change_preserves_history(tmp_path):
    session_factory = make_session_factory(tmp_path)
    with session_factory() as session:
        repository = FlightObservationRepository(session)

        first = make_observation(fare=5482.0)
        second = make_observation(fare=6200.0)

        repository.save_if_new(first)
        repository.save_if_new(second)

        rows = session.scalars(select(FlightObservationModel)).all()
        assert len(rows) == 2


def test_scheduler_skips_duplicates_on_second_run(tmp_path, monkeypatch):
    session_factory = make_session_factory(tmp_path)
    monkeypatch.setattr(scheduler_module, "SessionLocal", session_factory)
    monkeypatch.setattr(scheduler_module, "create_database", lambda: None)

    async def run():
        first = await scheduler_module.collect_and_store(
            origin="DEL",
            destination="BOM",
            travel_date=date(2026, 9, 10),
        )
        second = await scheduler_module.collect_and_store(
            origin="DEL",
            destination="BOM",
            travel_date=date(2026, 9, 10),
        )
        return first, second

    first_run, second_run = asyncio.run(run())

    assert len(first_run) == 3
    assert len(second_run) == 0
    assert scheduler_module.collect_and_store.last_summary.total_collected == 3
    assert scheduler_module.collect_and_store.last_summary.duplicates_skipped == 3
    assert scheduler_module.collect_and_store.last_summary.new_records_stored == 0


def test_get_flight_history_returns_ordered_records(tmp_path):
    session_factory = make_session_factory(tmp_path)
    with session_factory() as session:
        repository = FlightObservationRepository(session)

        first = make_observation(
            fare=5482.0,
            collected_at=datetime(2026, 9, 1, 9, 0, tzinfo=timezone.utc),
        )
        second = make_observation(
            fare=6200.0,
            collected_at=datetime(2026, 9, 1, 9, 5, tzinfo=timezone.utc),
        )
        third = make_observation(
            fare=5900.0,
            collected_at=datetime(2026, 9, 1, 9, 2, tzinfo=timezone.utc),
        )

        repository.save_if_new(first)
        repository.save_if_new(second)
        repository.save_if_new(third)

        history = repository.get_flight_history(
            source="source_a",
            flight_number="6E-123",
            origin="DEL",
            destination="BOM",
            travel_date=date(2026, 9, 10),
        )

        assert [record.fare for record in history] == [5482.0, 5900.0, 6200.0]


def test_scheduler_isolates_source_failures(tmp_path, monkeypatch):
    session_factory = make_session_factory(tmp_path)
    monkeypatch.setattr(scheduler_module, "SessionLocal", session_factory)
    monkeypatch.setattr(scheduler_module, "create_database", lambda: None)

    class FailingSource:
        async def fetch(self, origin, destination, travel_date):
            raise RuntimeError("upstream outage")

    class SuccessSource:
        async def fetch(self, origin, destination, travel_date):
            return [{
                "source": "mock_source",
                "airline": "IndiGo",
                "flight_number": "6E-789",
                "origin": origin,
                "destination": destination,
                "travel_date": travel_date.isoformat(),
                "departure_time": "09:00:00",
                "stops": 0,
                "fare": 5000.0,
                "currency": "INR",
                "collected_at": datetime.now(timezone.utc).isoformat(),
            }]

    monkeypatch.setattr(scheduler_module, "SourceA", FailingSource)
    monkeypatch.setattr(scheduler_module, "SourceB", SuccessSource)
    monkeypatch.setattr(scheduler_module, "SourceC", SuccessSource)

    async def run():
        return await scheduler_module.collect_and_store(
            origin="DEL",
            destination="BOM",
            travel_date=date(2026, 9, 10),
        )

    records = asyncio.run(run())

    assert len(records) == 2
    assert scheduler_module.collect_and_store.last_summary.failed_sources == 1
    assert scheduler_module.collect_and_store.last_summary.successful_sources == 2
