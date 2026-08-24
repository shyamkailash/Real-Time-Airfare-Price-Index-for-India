from ingestion.schemas.flight_observation import FlightObservation


def validate_observation(
    observation: FlightObservation,
) -> FlightObservation:

    if observation.origin == observation.destination:
        raise ValueError(
            "Origin and destination cannot be the same."
        )

    if observation.fare <= 0:
        raise ValueError(
            "Fare must be greater than zero."
        )

    if observation.stops < 0:
        raise ValueError(
            "Stops cannot be negative."
        )

    return observation