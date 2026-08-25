from datetime import date

from backend.storage.database import SessionLocal
from backend.storage.repository import FlightObservationRepository


def main():
    session = SessionLocal()

    try:
        repository = FlightObservationRepository(session)

        observations = repository.get_by_route(
            origin="DEL",
            destination="BOM",
            travel_date=date(2026, 9, 10),
        )

        print("\n" + "=" * 60)
        print("DATABASE RETRIEVAL TEST")
        print("=" * 60)

        print(f"Total observations retrieved: {len(observations)}")

        for observation in observations:
            print(
                {
                    "id": observation.id,
                    "source": observation.source,
                    "airline": observation.airline,
                    "fare": observation.fare,
                    "currency": observation.currency,
                }
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()  