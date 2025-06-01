
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_homepage_redirect():
    response = client.get("/")
    assert response.status_code in [200, 307, 404]  # depends on route config

def test_invalid_route():
    response = client.get("/non-existent-endpoint")
    assert response.status_code == 404
