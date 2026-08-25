from datetime import date

from backend.ingestion.collectors.base_collector import BaseCollector
from backend.ingestion.normalizers.flight_normalizer import normalize_flight
from backend.ingestion.schemas.flight_observation import FlightObservation
from backend.ingestion.validators.observation_validator import validate_observation


class FlightCollector(BaseCollector):

    def __init__(self, source):
        self.source = source

    async def collect(
        self,
        origin: str,
        destination: str,
        travel_date: date
    ) -> list[FlightObservation]:
        raw_flights = await self.source.fetch(
            origin,
            destination,
            travel_date,
        )

        observations: list[FlightObservation] = []

        for raw_flight in raw_flights:
            observation = normalize_flight(raw_flight)
            validated_observation = validate_observation(observation)
            observations.append(validated_observation)

        return observations