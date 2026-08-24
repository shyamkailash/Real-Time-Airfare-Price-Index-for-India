"""
Test Health Endpoint
"""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    """Test the /api/health endpoint returns ok status"""
    response = client.get("/api/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_check_response_structure():
    """Test the /api/health endpoint response structure"""
    response = client.get("/api/health")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert isinstance(data["status"], str)
