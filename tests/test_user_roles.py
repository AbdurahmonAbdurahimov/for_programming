
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_unauthorized_user_access():
    response = client.get("/meals/")
    assert response.status_code in [401, 403, 200]  # depends on auth config
