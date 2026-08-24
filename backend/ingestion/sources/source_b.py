from datetime import date, datetime, timezone
import logging

from .base import BaseSource


logger = logging.getLogger(__name__)


class SourceB(BaseSource):
    """
    Source B airfare collector.

    Currently implemented as a test collector.
    Replace the fetch logic with the actual permitted API/web
    collection mechanism later.
    """

    async def fetch(
        self,
        origin: str,
        destination: str,
        travel_date: date,
    ) -> list[dict]:

        logger.info(
            "Fetching flights from Source B: %s -> %s for %s",
            origin,
            destination,
            travel_date,
        )

        return [
            {
                "source": "source_b",
                "airline": "Air India",
                "flight_number": "AI-456",
                "origin": origin,
                "destination": destination,
                "travel_date": travel_date.isoformat(),
                "departure_time": "10:15:00",
                "stops": 0,
                "fare": 6235.0,
                "currency": "INR",
                "collected_at": datetime.now(timezone.utc).isoformat(),
            }
        ]