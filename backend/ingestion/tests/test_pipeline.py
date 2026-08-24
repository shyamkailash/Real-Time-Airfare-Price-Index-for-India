import asyncio
from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ingestion.scheduler.jobs as jobs_module
from storage.database import Base


@pytest.mark.asyncio
async def test_scheduler_collects_all_sources_once(tmp_path, monkeypatch):
    db_path = tmp_path / "pipeline_test.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    monkeypatch.setattr(jobs_module, "SessionLocal", session_factory)
    monkeypatch.setattr(jobs_module, "create_database", lambda: None)

    records = await jobs_module.collect_and_store(
        origin="DEL",
        destination="BOM",
        travel_date=date(2026, 9, 10),
    )

    assert len(records) == 3
    assert {record.source for record in records} == {
        "source_a",
        "source_b",
        "source_c",
    }
    assert {record.origin for record in records} == {"DEL"}
    assert {record.destination for record in records} == {"BOM"}
