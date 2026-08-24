"""
Tests for routes API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRoutesEndpoint:
    """Test suite for /api/routes endpoint."""
    
    def test_get_routes_returns_200(self):
        """Test that GET /api/routes returns HTTP 200."""
        response = client.get("/api/routes")
        assert response.status_code == 200
    
    def test_get_routes_returns_json_list(self):
        """Test that GET /api/routes returns a JSON list."""
        response = client.get("/api/routes")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_route_contains_required_fields(self):
        """Test that each route contains id, origin, and destination."""
        response = client.get("/api/routes")
        assert response.status_code == 200
        
        data = response.json()
        for route in data:
            assert "id" in route
            assert "origin" in route
            assert "destination" in route
            
            # Verify types
            assert isinstance(route["id"], int)
            assert isinstance(route["origin"], str)
            assert isinstance(route["destination"], str)
            
            # Verify IATA code format (3 characters)
            assert len(route["origin"]) == 3
            assert len(route["destination"]) == 3
    
    def test_route_structure(self):
        """Test that routes have the expected structure."""
        response = client.get("/api/routes")
        data = response.json()
        
        # Test first route as example
        if len(data) > 0:
            first_route = data[0]
            assert first_route["id"] >= 1
            assert first_route["origin"].isupper()
            assert first_route["destination"].isupper()
    
    def test_multiple_routes_returned(self):
        """Test that multiple routes are returned."""
        response = client.get("/api/routes")
        data = response.json()
        
        # Should have multiple routes in mock data
        assert len(data) >= 2
