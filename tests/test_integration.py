import os
import pytest
from fastapi.testclient import TestClient

from backend.main import app

os.environ["AUTH_ENABLED"] = "false"

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data

def test_ready_endpoint():
    response = client.get("/ready")
    assert response.status_code in [200, 503]

@pytest.mark.asyncio
async def test_query_endpoint_validation():
    response = client.post(
        "/query",
        json={"question": "DELETE FROM customers"}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_query_endpoint_empty():
    response = client.post(
        "/query",
        json={"question": ""}
    )
    assert response.status_code == 422

def test_cors_headers():
    response = client.options("/query")
    assert response.status_code in [200, 405]
