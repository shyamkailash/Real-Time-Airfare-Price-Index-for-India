from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from ingestion.schemas.flight_observation import FlightObservation
from storage.models import FlightObservationModel


class FlightObservationRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(
        self,
        observation: FlightObservation,
    ) -> FlightObservationModel:

        record = FlightObservationModel(
            source=observation.source,
            airline=observation.airline,
            origin=observation.origin,
            destination=observation.destination,
            travel_date=observation.travel_date,
            departure_time=observation.departure_time,
            stops=observation.stops,
            fare=observation.fare,
            currency=observation.currency,
            collected_at=observation.collected_at,
        )

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)

        return record

    def save_many(
        self,
        observations: list[FlightObservation],
    ) -> list[FlightObservationModel]:

        records = [
            FlightObservationModel(
                source=observation.source,
                airline=observation.airline,
                origin=observation.origin,
                destination=observation.destination,
                travel_date=observation.travel_date,
                departure_time=observation.departure_time,
                stops=observation.stops,
                fare=observation.fare,
                currency=observation.currency,
                collected_at=observation.collected_at,
            )
            for observation in observations
        ]

        self.session.add_all(records)
        self.session.commit()

        for record in records:
            self.session.refresh(record)

        return records

    def get_by_route(
        self,
        origin: str,
        destination: str,
        travel_date: date,
    ) -> list[FlightObservationModel]:

        statement = (
            select(FlightObservationModel)
            .where(
                FlightObservationModel.origin == origin.upper(),
                FlightObservationModel.destination == destination.upper(),
                FlightObservationModel.travel_date == travel_date,
            )
            .order_by(FlightObservationModel.fare.asc())
        )

        return list(self.session.scalars(statement).all())