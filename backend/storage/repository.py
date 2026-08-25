from datetime import date, datetime

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from backend.ingestion.schemas.flight_observation import FlightObservation
from backend.storage.models import FlightObservationModel


class FlightObservationRepository:

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def _duplicate_key(observation: FlightObservation) -> tuple:
        return (
            observation.source,
            observation.airline,
            observation.flight_number,
            observation.origin.upper(),
            observation.destination.upper(),
            observation.travel_date,
            observation.departure_time,
            observation.stops,
            observation.fare,
            observation.currency.upper(),
        )

    @staticmethod
    def _model_from_observation(
        observation: FlightObservation,
    ) -> FlightObservationModel:
        return FlightObservationModel(
            source=observation.source,
            airline=observation.airline,
            flight_number=observation.flight_number,
            origin=observation.origin.upper(),
            destination=observation.destination.upper(),
            travel_date=observation.travel_date,
            departure_time=observation.departure_time,
            stops=observation.stops,
            fare=observation.fare,
            currency=observation.currency.upper(),
            collected_at=observation.collected_at,
        )

    def exists(self, observation: FlightObservation) -> bool:
        statement = select(FlightObservationModel.id).where(
            FlightObservationModel.source == observation.source,
            FlightObservationModel.airline == observation.airline,
            FlightObservationModel.flight_number == observation.flight_number,
            FlightObservationModel.origin == observation.origin.upper(),
            FlightObservationModel.destination == observation.destination.upper(),
            FlightObservationModel.travel_date == observation.travel_date,
            FlightObservationModel.departure_time == observation.departure_time,
            FlightObservationModel.stops == observation.stops,
            FlightObservationModel.fare == observation.fare,
            FlightObservationModel.currency == observation.currency.upper(),
        )

        return self.session.scalar(statement) is not None

    def save(
        self,
        observation: FlightObservation,
    ) -> FlightObservationModel:

        record = self._model_from_observation(observation)

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)

        return record

    def save_if_new(
        self,
        observation: FlightObservation,
    ) -> FlightObservationModel | None:
        if self.exists(observation):
            return None
        return self.save(observation)

    def save_many(
        self,
        observations: list[FlightObservation],
    ) -> list[FlightObservationModel]:

        records = [
            self._model_from_observation(observation)
            for observation in observations
        ]

        self.session.add_all(records)
        self.session.commit()

        for record in records:
            self.session.refresh(record)

        return records

    def save_many_if_new(
        self,
        observations: list[FlightObservation],
    ) -> list[FlightObservationModel]:
        if not observations:
            return []

        duplicate_candidates = [
            and_(
                FlightObservationModel.source == observation.source,
                FlightObservationModel.airline == observation.airline,
                FlightObservationModel.flight_number == observation.flight_number,
                FlightObservationModel.origin == observation.origin.upper(),
                FlightObservationModel.destination == observation.destination.upper(),
                FlightObservationModel.travel_date == observation.travel_date,
                FlightObservationModel.departure_time == observation.departure_time,
                FlightObservationModel.stops == observation.stops,
                FlightObservationModel.fare == observation.fare,
                FlightObservationModel.currency == observation.currency.upper(),
            )
            for observation in observations
        ]

        statement = select(FlightObservationModel).where(or_(*duplicate_candidates))
        existing_records = self.session.scalars(statement).all()
        existing_keys = {
            (
                record.source,
                record.airline,
                record.flight_number,
                record.origin,
                record.destination,
                record.travel_date,
                record.departure_time,
                record.stops,
                record.fare,
                record.currency,
            )
            for record in existing_records
        }

        new_observations = []
        for observation in observations:
            if self._duplicate_key(observation) in existing_keys:
                continue
            new_observations.append(observation)

        if not new_observations:
            return []

        records = [
            self._model_from_observation(observation)
            for observation in new_observations
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

    def get_history(
        self,
        origin: str,
        destination: str,
        travel_date: date | None = None,
    ) -> list[FlightObservationModel]:
        statement = select(FlightObservationModel).where(
            FlightObservationModel.origin == origin.upper(),
            FlightObservationModel.destination == destination.upper(),
        )

        if travel_date is not None:
            statement = statement.where(
                FlightObservationModel.travel_date == travel_date,
            )

        statement = statement.order_by(
            FlightObservationModel.travel_date.asc(),
            FlightObservationModel.collected_at.asc(),
        )

        return list(self.session.scalars(statement).all())

    def get_flight_history(
        self,
        source: str,
        flight_number: str,
        origin: str,
        destination: str,
        travel_date: date,
    ) -> list[FlightObservationModel]:
        statement = (
            select(FlightObservationModel)
            .where(
                FlightObservationModel.source == source,
                FlightObservationModel.flight_number == flight_number,
                FlightObservationModel.origin == origin.upper(),
                FlightObservationModel.destination == destination.upper(),
                FlightObservationModel.travel_date == travel_date,
            )
            .order_by(FlightObservationModel.collected_at.asc())
        )

        return list(self.session.scalars(statement).all())
    def get_observations(
        self,
        page: int = 1,
        page_size: int = 10,
        q: str | None = None,
        origin: str | None = None,
        destination: str | None = None,
        airline: str | None = None,
        source: str | None = None,
    ) -> tuple[list[FlightObservationModel], int]:
        page = max(page, 1)
        page_size = max(min(page_size, 100), 1)

        statement = select(FlightObservationModel)

        if q:
            search = f"%{q.strip()}%"
            statement = statement.where(
                or_(
                    FlightObservationModel.airline.ilike(search),
                    FlightObservationModel.flight_number.ilike(search),
                    FlightObservationModel.origin.ilike(search),
                    FlightObservationModel.destination.ilike(search),
                    FlightObservationModel.source.ilike(search),
                )
            )

        if origin:
            statement = statement.where(
                FlightObservationModel.origin == origin.upper()
            )

        if destination:
            statement = statement.where(
                FlightObservationModel.destination == destination.upper()
            )

        if airline:
            statement = statement.where(
                FlightObservationModel.airline == airline
            )

        if source:
            statement = statement.where(
                FlightObservationModel.source == source
            )

        count_statement = select(func.count()).select_from(
            statement.subquery()
        )

        total = self.session.scalar(count_statement) or 0

        statement = (
            statement
            .order_by(FlightObservationModel.collected_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        rows = list(self.session.scalars(statement).all())

        return rows, total
