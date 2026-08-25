from abc import ABC, abstractmethod
from datetime import date

from backend.ingestion.schemas.flight_observation import FlightObservation


class BaseCollector(ABC):

    @abstractmethod
    async def collect(
        self,
        origin: str,
        destination: str,
        travel_date: date
    ) -> list[FlightObservation]:
        """Return standardized flight observations."""
        pass