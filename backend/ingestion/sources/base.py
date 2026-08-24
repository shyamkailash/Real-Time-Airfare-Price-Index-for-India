from abc import ABC, abstractmethod
from datetime import date


class BaseSource(ABC):

    @abstractmethod
    async def fetch(
        self,
        origin: str,
        destination: str,
        travel_date: date
    ):
        """Fetch raw flight data from the source."""
        pass