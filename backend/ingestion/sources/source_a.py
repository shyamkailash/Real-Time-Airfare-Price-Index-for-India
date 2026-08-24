from time import timezone
from datetime import datetime, timezone

from ingestion.utils.retry import retry_on_failure
from ingestion.utils.logging import setup_logger


logger = setup_logger(__name__)


class SourceA:

    @retry_on_failure
    async def fetch(self, origin, destination, travel_date):

        logger.info(
            "Fetching flights: %s -> %s for %s",
            origin,
            destination,
            travel_date
        )

        return [
            {
                "source": "source_a",
                "airline": "IndiGo",
                "origin": origin,
                "destination": destination,
                "travel_date": str(travel_date),
                "departure_time": "08:30:00",
                "stops": 0,
                "fare": 5482.0,
                "currency": "INR",
                "collected_at": datetime.now(timezone.utc).isoformat()
            }
        ]