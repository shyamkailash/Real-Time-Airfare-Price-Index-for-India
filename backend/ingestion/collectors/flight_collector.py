from datetime import date, datetime, time, timezone
from ingestion.validators.observation_validator import validate_observation
from ingestion.collectors.base_collector import BaseCollector
from ingestion.schemas.flight_observation import FlightObservation


class FlightCollector(BaseCollector):

    def __init__(self, source):
        self.source = source

    async def collect(
        self,
        origin: str,
        destination: str,
        travel_date: date
    ) -> list[FlightObservation]:

        # Step 1: Get raw data from the source
        raw_flights = await self.source.fetch(
            origin,
            destination,
            travel_date
        )

        observations = []

        # Step 2: Convert raw data into standard format
        for flight in raw_flights:

            observation = FlightObservation(
                source="source_a",
                airline=flight["carrier"],
                origin=flight["from"].upper(),
                destination=flight["to"].upper(),
                travel_date=date.fromisoformat(flight["date"]),
                departure_time=time.fromisoformat(
                    flight["departure"]
                ),
                stops=flight["stops"],
                fare=float(flight["price"]),
                currency=flight["currency"].upper(),
                collected_at=datetime.now(timezone.utc)
            )

            validated_observation = validate_observation(observation)
            observations.append(validated_observation)
            
        return observations