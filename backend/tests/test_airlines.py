"""
Tests for airlines API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_airlines_returns_200():
    """
    Test that GET /api/airlines returns HTTP 200.
    """
    response = client.get("/api/airlines")
    assert response.status_code == 200


def test_get_airlines_returns_json_list():
    """
    Test that GET /api/airlines returns a JSON list.
    """
    response = client.get("/api/airlines")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_airlines_response_structure():
    """
    Test that every airline contains id, iata_code, and name.
    """
    response = client.get("/api/airlines")
    assert response.status_code == 200
    data = response.json()
    
    # Ensure we have at least one airline in the response
    assert len(data) > 0
    
    # Verify each airline has the required fields
    for airline in data:
        assert "id" in airline
        assert "iata_code" in airline
        assert "name" in airline
        assert isinstance(airline["id"], int)
        assert isinstance(airline["iata_code"], str)
        assert isinstance(airline["name"], str)


def test_get_airlines_mock_data():
    """
    Test that the mock data is returned correctly.
    This test is temporary and should be updated when real database is connected.
    """
    response = client.get("/api/airlines")
    assert response.status_code == 200
    data = response.json()
    
    # Verify we have the expected mock airlines
    assert len(data) == 3
    
    # Check specific mock data
    airline_codes = [airline["iata_code"] for airline in data]
    assert "6E" in airline_codes  # IndiGo
    assert "AI" in airline_codes  # Air India
    assert "UK" in airline_codes  # Vistara
