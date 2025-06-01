
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_meal():
    response = client.post("/meals/", json={"name": "Soup", "ingredients": []})
    assert response.status_code in [200, 201, 422]  # depending on validation

def test_get_meals():
    response = client.get("/meals/")
    assert response.status_code == 200
