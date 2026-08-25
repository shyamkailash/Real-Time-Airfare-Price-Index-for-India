from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.airfare import router as airfare_router

app = FastAPI(
    title="Real-Time Airfare Price Index for India",
    version="1.0.0",
    description="Historical airfare collection, validation, deduplication, and price index API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(airfare_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Real-Time Airfare Price Index for India"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
