from fastapi.testclient import TestClient
from application.main import app

client = TestClient(app)

def test_manifest_json():
    response = client.get("/static/manifest.json")
    assert response.status_code == 200
    data = response.json()
    assert data.get("name") == "Task & Habit Tracker"
    assert "icons" in data

def test_service_worker():
    response = client.get("/static/js/service-worker.js")
    assert response.status_code == 200
    assert b"self.addEventListener('install'" in response.content
