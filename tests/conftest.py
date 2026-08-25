import pytest

from backend.database.session import get_db


@pytest.fixture
def db():
    session = next(get_db())

    try:
        yield session
    finally:
        session.rollback()
        session.close()