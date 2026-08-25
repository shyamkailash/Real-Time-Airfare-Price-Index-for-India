from __future__ import annotations

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from backend.api.schemas.airfare import (
    FlightPriceIndex,
    ObservationListResponse,
    ObservationResponse,
    RouteHistoryResponse,
    RoutePriceIndex,
)
from backend.storage.database import SessionLocal, create_database
from backend.storage.repository import FlightObservationRepository

router = APIRouter(prefix="/api", tags=["airfare"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/routes")
def get_routes() -> list[dict[str, str]]:
    create_database()
    with SessionLocal() as session:
        rows, _ = FlightObservationRepository(session).get_observations(page_size=100)
    routes = {}
    for record in rows:
        route_id = f"{record.origin}-{record.destination}"
        routes[route_id] = {
            "id": route_id,
            "origin": record.origin,
            "destination": record.destination,
            "travel_date": record.travel_date.isoformat(),
        }
    return list(routes.values())


@router.get("/airlines")
def get_airlines() -> list[dict[str, float | int | str]]:
    create_database()
    with SessionLocal() as session:
        rows, _ = FlightObservationRepository(session).get_observations(page_size=100)
    grouped: dict[str, list[float]] = {}
    for record in rows:
        grouped.setdefault(record.airline, []).append(float(record.fare))
    return [
        {
            "id": airline.lower().replace(" ", "-"),
            "name": airline,
            "airline": airline,
            "observation_count": len(fares),
            "average_fare": sum(fares) / len(fares),
            "minimum_fare": min(fares),
            "maximum_fare": max(fares),
            "index": 100.0,
            "yoyChange": 0.0,
        }
        for airline, fares in sorted(grouped.items())
    ]


@router.get("/fares")
def get_fares() -> list[dict[str, object]]:
    response = get_observations(page=1, page_size=100)
    return [observation.model_dump(mode="json") for observation in response.data]


@router.get("/index/current")
def get_current_index() -> dict[str, float | int | str]:
    response = get_observations(page=1, page_size=100)
    fares = [observation.fare for observation in response.data]
    average_fare = sum(fares) / len(fares) if fares else 0.0
    index = average_fare / 50 if average_fare else 100.0
    return {
        "index": index,
        "date": "2026-09-10",
        "change": 0.0,
        "yoyChange": 0.0,
        "momChange": 0.0,
        "base_period": "2025-01",
        "basePeriod": "2025-01",
        "sample_count": len(fares),
    }


@router.get("/index/history")
def get_index_history() -> list[dict[str, float | str]]:
    current = get_current_index()
    return [
        {"date": "2025-01-01", "value": 100.0},
        {"date": "2026-09-10", "value": float(current["index"])},
    ]


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
