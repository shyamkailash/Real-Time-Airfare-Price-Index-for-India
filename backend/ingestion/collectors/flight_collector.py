from datetime import date

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
            observation = FlightObservation(**flight)

            # Apply business validation rules
            validated_observation = validate_observation(
                observation
            )

            observations.append(validated_observation)

        return observations