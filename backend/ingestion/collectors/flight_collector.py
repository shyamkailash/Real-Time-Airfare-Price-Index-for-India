from datetime import date, datetime, time, timezone

from ingestion.collectors.base_collector import BaseCollector
from ingestion.schemas.flight_observation import FlightObservation
from ingestion.validators.observation_validator import validate_observation


class FlightCollector(BaseCollector):

    def __init__(self, source):
        self.source = source

    async def collect(
        self,
        origin: str,
        destination: str,
        travel_date: date
    ) -> list[FlightObservation]:

        # Fetch canonical observations from the configured source
        raw_flights = await self.source.fetch(
            origin,
            destination,
            travel_date
        )

        observations = []

        for flight in raw_flights:

            # Convert source data into the canonical Pydantic schema
            observation = FlightObservation(
                source=flight["source"],
                airline=flight["airline"],
                flight_number=flight.get("flight_number"),
                origin=flight["origin"].upper(),
                destination=flight["destination"].upper(),
                travel_date=date.fromisoformat(flight["travel_date"]),
                departure_time=time.fromisoformat(
                    flight["departure_time"]
                ),
                stops=flight["stops"],
                fare=float(flight["fare"]),
                currency=flight["currency"].upper(),
                collected_at=datetime.now(timezone.utc),
            )
            # Apply business validation rules
            validated_observation = validate_observation(
                observation
            )

            observations.append(validated_observation)

        return observations