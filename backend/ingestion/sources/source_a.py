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
                "carrier": "IndiGo",
                "from": origin,
                "to": destination,
                "date": str(travel_date),
                "departure": "08:30",
                "stops": 0,
                "price": 5482,
                "currency": "INR"
            }
        ]