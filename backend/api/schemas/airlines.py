"""
Pydantic schemas for airlines API endpoints.
"""
from pydantic import BaseModel


class AirlineResponse(BaseModel):
    """
    Response schema for airline data.
    """
    id: int
    iata_code: str
    name: str
