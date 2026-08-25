"""
Tests for fares API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_get_fares_returns_200():
    """
    Test that GET /api/fares returns HTTP 200.
    """
    response = client.get("/api/fares")
    assert response.status_code == 200


def test_get_fares_returns_json_list():
    """
    Test that GET /api/fares returns a JSON list.
    """
    response = client.get("/api/fares")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_fares_at_least_three_observations():
    """
    Test that at least 3 observations are returned.
    """
    response = client.get("/api/fares")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_get_fares_response_structure():
    """
    Test that each fare contains all required fields.
    """
    response = client.get("/api/fares")
    assert response.status_code == 200
    data = response.json()
    
    # Ensure we have at least one fare in the response
    assert len(data) > 0
    
    # Verify each fare has the required fields
    for fare in data:
        assert "id" in fare
        assert "source" in fare
        assert "airline" in fare
        assert "origin" in fare
        assert "destination" in fare
        assert "travel_date" in fare
        assert "departure_time" in fare
        assert "stops" in fare
        assert "fare" in fare
        assert "currency" in fare
        assert "collected_at" in fare


def test_get_fares_field_types():
    """
    Test that fare fields have correct types.
    """
    response = client.get("/api/fares")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) > 0
    
    for fare in data:
        # Test numeric fare
        assert isinstance(fare["fare"], (int, float))
        assert fare["fare"] > 0
        
        # Test integer stops
        assert isinstance(fare["stops"], int)
        assert fare["stops"] >= 0
        
        # Test string fields
        assert isinstance(fare["id"], int)
        assert isinstance(fare["source"], str)
        assert isinstance(fare["airline"], str)
        assert isinstance(fare["origin"], str)
        assert isinstance(fare["destination"], str)
        assert isinstance(fare["currency"], str)


def test_get_fares_currency_is_inr():
    """
    Test that currency is INR for all fares.
    """
    response = client.get("/api/fares")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) > 0
    
    for fare in data:
        assert fare["currency"] == "INR"


def test_get_fares_mock_data():
    """
    Test that the mock data is returned correctly.
    This test is temporary and should be updated when real database is connected.
    """
    response = client.get("/api/fares")
    assert response.status_code == 200
    data = response.json()
    
    # Verify we have the expected number of mock fares
    assert len(data) >= 3
    
    # Check specific mock data elements
    airlines = [fare["airline"] for fare in data]
    assert "IndiGo" in airlines
    assert "Air India" in airlines
    assert "Vistara" in airlines
    
    # Verify routes exist
    routes = [(fare["origin"], fare["destination"]) for fare in data]
    assert ("DEL", "BOM") in routes
