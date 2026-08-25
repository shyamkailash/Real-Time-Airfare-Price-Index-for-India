from datetime import date, datetime, timezone

from ingestion.sources.base import BaseSource
from ingestion.utils.logging import setup_logger
from ingestion.utils.retry import retry_on_failure


logger = setup_logger(__name__)


class SourceA(BaseSource):

    @retry_on_failure
    async def fetch(
        self,
        origin: str,
        destination: str,
        travel_date: date,
    ) -> list[dict]:

        logger.info(
            "Fetching flights: %s -> %s for %s",
            origin,
            destination,
            travel_date,
        )

        return [
            {
                "source": "source_a",
                "airline": "IndiGo",
                "flight_number": "6E-123",
                "origin": origin,
                "destination": destination,
                "travel_date": travel_date.isoformat(),
                "departure_time": "08:30:00",
                "stops": 0,
                "fare": 5482.0,
                "currency": "INR",
                "collected_at": datetime.now(timezone.utc).isoformat(),
            }
        ]