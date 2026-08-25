from __future__ import annotations

from fastapi import FastAPI

from api.routes.airfare import router as airfare_router

app = FastAPI(
    title="Real-Time Airfare Price Index for India",
    version="1.0.0",
    description="Historical airfare collection, validation, deduplication, and price index API.",
)

app.include_router(airfare_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Real-Time Airfare Price Index for India"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
