from ingestion.schemas.flight_observation import FlightObservation


def validate_observation(
    observation: FlightObservation,
) -> FlightObservation:

    if observation.origin == observation.destination:
        raise ValueError(
            "Origin and destination cannot be the same."
        )

    if len(observation.origin) != 3 or not observation.origin.isalpha():
        raise ValueError(
            "Origin must be a 3-character uppercase airport code."
        )

    if len(observation.destination) != 3 or not observation.destination.isalpha():
        raise ValueError(
            "Destination must be a 3-character uppercase airport code."
        )

    if len(observation.currency) != 3 or not observation.currency.isalpha():
        raise ValueError(
            "Currency must be a 3-character uppercase code."
        )

    if observation.fare <= 0:
        raise ValueError(
            "Fare must be greater than zero."
        )

    if observation.stops < 0:
        raise ValueError(
            "Stops cannot be negative."
        )

    if observation.collected_at.tzinfo is None or observation.collected_at.utcoffset() is None:
        raise ValueError(
            "collected_at must be timezone-aware."
        )

    if observation.departure_time is not None:
        try:
            observation.departure_time.isoformat()
        except ValueError as exc:  # pragma: no cover - defensive validation
            raise ValueError("departure_time must be a valid time.") from exc

    return observation