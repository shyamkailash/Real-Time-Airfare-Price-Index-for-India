from __future__ import annotations

from datetime import date

from storage.database import SessionLocal
from storage.repository import FlightObservationRepository


class AirfareService:
    @staticmethod
    def calculate_route_index(
        origin: str,
        destination: str,
        travel_date: date,
    ) -> dict[str, float | int | str]:
        with SessionLocal() as session:
            repository = FlightObservationRepository(session)
            observations = repository.get_history(
                origin=origin,
                destination=destination,
                travel_date=travel_date,
            )

        if not observations:
            raise ValueError("No observations found for the requested route.")

        fares = [record.fare for record in observations]
        latest_fare = fares[-1]
        historical_average = sum(fares) / len(fares)
        historical_min = min(fares)
        historical_max = max(fares)
        price_index = (latest_fare / historical_average * 100) if historical_average else 0.0
        trend = "low" if price_index < 95 else "high" if price_index > 105 else "neutral"

        return {
            "origin": origin.upper(),
            "destination": destination.upper(),
            "travel_date": travel_date,
            "latest_fare": latest_fare,
            "historical_average": historical_average,
            "historical_min": historical_min,
            "historical_max": historical_max,
            "sample_count": len(fares),
            "price_index": price_index,
            "trend": trend,
        }

    @staticmethod
    def calculate_flight_index(
        source: str,
        flight_number: str,
        origin: str,
        destination: str,
        travel_date: date,
    ) -> dict[str, float | int | str | None]:
        with SessionLocal() as session:
            repository = FlightObservationRepository(session)
            observations = repository.get_flight_history(
                source=source,
                flight_number=flight_number,
                origin=origin,
                destination=destination,
                travel_date=travel_date,
            )

        if not observations:
            raise ValueError("No historical observations found for the requested flight.")

        fares = [record.fare for record in observations]
        latest_fare = fares[-1]
        historical_average = sum(fares) / len(fares)
        historical_min = min(fares)
        historical_max = max(fares)
        price_index = (latest_fare / historical_average * 100) if historical_average else 0.0
        trend = "low" if price_index < 95 else "high" if price_index > 105 else "neutral"

        return {
            "source": source,
            "airline": observations[0].airline,
            "flight_number": flight_number,
            "origin": origin.upper(),
            "destination": destination.upper(),
            "travel_date": travel_date,
            "latest_fare": latest_fare,
            "historical_average": historical_average,
            "historical_min": historical_min,
            "historical_max": historical_max,
            "sample_count": len(fares),
            "price_index": price_index,
            "trend": trend,
        }
