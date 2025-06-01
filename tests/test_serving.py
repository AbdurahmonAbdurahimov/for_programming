
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_serve_meal_invalid():
    response = client.post("/serve/", json={"meal_id": 9999})
    assert response.status_code in [400, 404, 422]
