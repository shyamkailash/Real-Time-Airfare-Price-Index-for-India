from abc import ABC, abstractmethod
from datetime import date
from typing import Any


class BaseSource(ABC):
    """
    Abstract interface for all airfare data sources.

    Every source must implement the async fetch() method and
    return raw flight data that can later be normalized.
    """

    @abstractmethod
    async def fetch(
        self,
        origin: str,
        destination: str,
        travel_date: date,
    ) -> list[dict[str, Any]]:
        """
        Fetch raw flight data from the source.

        Args:
            origin: IATA origin airport code, e.g. DEL.
            destination: IATA destination airport code, e.g. BOM.
            travel_date: Date of travel.

        Returns:
            A list of raw flight records.
        """
        raise NotImplementedError