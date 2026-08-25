from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.database.connection import Base, SessionLocal, engine


def initialize_database() -> None:
    from backend.database import models
    from backend.database.models.airline import Airline
    from backend.database.models.airport import Airport
    from backend.database.models.route import Route

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.query(Airport).count() == 0:
            db.add_all([
                Airport(iata_code="DEL", name="Indira Gandhi International", city="Delhi", country="India"),
                Airport(iata_code="BOM", name="Chhatrapati Shivaji Maharaj International", city="Mumbai", country="India"),
                Airport(iata_code="BLR", name="Kempegowda International", city="Bengaluru", country="India"),
                Airport(iata_code="MAA", name="Chennai International", city="Chennai", country="India"),
            ])
            db.flush()
        if db.query(Airline).count() == 0:
            db.add_all([
                Airline(iata_code="6E", name="IndiGo"),
                Airline(iata_code="AI", name="Air India"),
                Airline(iata_code="QP", name="Akasa Air"),
            ])
            db.flush()
        if db.query(Route).count() == 0:
            airports = {airport.iata_code: airport.id for airport in db.query(Airport).all()}
            db.add_all([
                Route(origin_airport_id=airports["DEL"], destination_airport_id=airports["BOM"]),
                Route(origin_airport_id=airports["DEL"], destination_airport_id=airports["BLR"]),
                Route(origin_airport_id=airports["BOM"], destination_airport_id=airports["BLR"]),
                Route(origin_airport_id=airports["DEL"], destination_airport_id=airports["MAA"]),
            ])
        db.commit()


def get_db() -> Generator[Session, None, None]:
    initialize_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()