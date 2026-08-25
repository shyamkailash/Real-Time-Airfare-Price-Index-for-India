from __future__ import annotations

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from api.schemas.airfare import (
    FlightPriceIndex,
    ObservationListResponse,
    ObservationResponse,
    RouteHistoryResponse,
    RoutePriceIndex,
)
from storage.database import SessionLocal
from storage.repository import FlightObservationRepository

router = APIRouter(prefix="/api", tags=["airfare"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/observations", response_model=ObservationListResponse)
def get_observations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    q: str | None = Query(None),
    origin: str | None = Query(None, min_length=3, max_length=3),
    destination: str | None = Query(None, min_length=3, max_length=3),
    airline: str | None = Query(None),
    source: str | None = Query(None),
) -> ObservationListResponse:
    with SessionLocal() as session:
        repository = FlightObservationRepository(session)

        records, total = repository.get_observations(
            page=page,
            page_size=page_size,
            q=q,
            origin=origin,
            destination=destination,
            airline=airline,
            source=source,
        )

    observations = [
        ObservationResponse(
            id=record.id,
            source=record.source,
            airline=record.airline,
            flight_number=record.flight_number,
            origin=record.origin,
            destination=record.destination,
            travel_date=record.travel_date,
            departure_time=(
                record.departure_time.isoformat()
                if record.departure_time
                else None
            ),
            stops=record.stops,
            fare=record.fare,
            currency=record.currency,
            collected_at=record.collected_at,
        )
        for record in records
    ]

    return ObservationListResponse(
        data=observations,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/routes/{origin}/{destination}/{travel_date}",
    response_model=RouteHistoryResponse,
)
def get_route_history(
    origin: str,
    destination: str,
    travel_date: date,
) -> RouteHistoryResponse:
    with SessionLocal() as session:
        repository = FlightObservationRepository(session)
        observations = repository.get_history(
            origin=origin,
            destination=destination,
            travel_date=travel_date,
        )

    if not observations:
        raise HTTPException(status_code=404, detail="No observations found for the requested route.")

    route_observations = [
        ObservationResponse(
            id=record.id,
            source=record.source,
            airline=record.airline,
            flight_number=record.flight_number,
            origin=record.origin,
            destination=record.destination,
            travel_date=record.travel_date,
            departure_time=record.departure_time.isoformat() if record.departure_time else None,
            stops=record.stops,
            fare=record.fare,
            currency=record.currency,
            collected_at=record.collected_at,
        )
        for record in observations
    ]

    fares = [item.fare for item in route_observations]
    latest_fare = fares[-1]
    historical_average = sum(fares) / len(fares)
    historical_min = min(fares)
    historical_max = max(fares)
    price_index = (latest_fare / historical_average * 100) if historical_average else 0.0
    trend = "low" if price_index < 95 else "high" if price_index > 105 else "neutral"

    route_index = RoutePriceIndex(
        origin=origin.upper(),
        destination=destination.upper(),
        travel_date=travel_date,
        latest_fare=latest_fare,
        historical_average=historical_average,
        historical_min=historical_min,
        historical_max=historical_max,
        sample_count=len(fares),
        price_index=price_index,
        trend=trend,
    )

    return RouteHistoryResponse(
        route=f"{origin.upper()}->{destination.upper()}",
        origin=origin.upper(),
        destination=destination.upper(),
        travel_date=travel_date,
        observations=route_observations,
        index=route_index,
    )


@router.get("/flights/history", response_model=list[FlightPriceIndex])
def get_flight_history(
    source: str = Query(..., min_length=1),
    flight_number: str = Query(..., min_length=1),
    origin: str = Query(..., min_length=3, max_length=3),
    destination: str = Query(..., min_length=3, max_length=3),
    travel_date: date = Query(...),
) -> list[FlightPriceIndex]:
    with SessionLocal() as session:
        repository = FlightObservationRepository(session)
        observations = repository.get_flight_history(
            source=source,
            flight_number=flight_number,
            origin=origin,
            destination=destination,
            travel_date=travel_date,
        )

    if not observations:
        raise HTTPException(status_code=404, detail="No historical observations found for the requested flight.")

    result: list[FlightPriceIndex] = []
    for record in observations:
        fares = [obs.fare for obs in observations]
        latest_fare = fares[-1]
        historical_average = sum(fares) / len(fares)
        historical_min = min(fares)
        historical_max = max(fares)
        price_index = (latest_fare / historical_average * 100) if historical_average else 0.0
        trend = "low" if price_index < 95 else "high" if price_index > 105 else "neutral"

        result.append(
            FlightPriceIndex(
                source=record.source,
                airline=record.airline,
                flight_number=record.flight_number,
                origin=record.origin,
                destination=record.destination,
                travel_date=record.travel_date,
                latest_fare=latest_fare,
                historical_average=historical_average,
                historical_min=historical_min,
                historical_max=historical_max,
                sample_count=len(fares),
                price_index=price_index,
                trend=trend,
            )
        )

    return result
