from abc import ABC, abstractmethod
from typing import Any


class FareCollector(ABC):
    """Base interface for all fare data collectors."""

    @abstractmethod
    def collect(self) -> list[dict[str, Any]]:
        """Collect fare observations from the source."""
        raise NotImplementedError