
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_ingredient():
    response = client.post("/ingredients/", json={"name": "Potato", "quantity": 1000})
    assert response.status_code == 200
    assert response.json()["name"] == "Potato"

def test_get_ingredients():
    response = client.get("/ingredients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
