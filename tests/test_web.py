import pytest
import uuid
from fastapi.testclient import TestClient
from application.main import app

client = TestClient(app)

def test_landing_page():
    response = client.get("/")
    assert response.status_code == 200
    assert b"Task & Habit Tracker" in response.content

def test_register_and_login():
    # Generate a unique email address for each test run
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    
    # First, register a new user; do not follow redirects so we can inspect the redirect code.
    register_response = client.post(
        "/register",
        data={"email": unique_email, "password": "password123"},
        follow_redirects=False
    )
    # Expect a redirect (302)
    assert register_response.status_code == 302, f"Register failed: {register_response.text}"
    
    # Now, login using the same unique credentials; again, disable redirects.
    login_response = client.post(
        "/login",
        data={"email": unique_email, "password": "password123"},
        follow_redirects=False
    )
    assert login_response.status_code == 302, f"Login failed: {login_response.text}"

def test_task_crud():
    # Generate a unique email for this test
    unique_email = f"taskuser_{uuid.uuid4().hex[:8]}@example.com"
    # Register a test user (disable redirects for clarity)
    client.post("/register", data={"email": unique_email, "password": "password123"}, follow_redirects=False)
    # Create a task
    create_response = client.post("/create_task", data={"title": "Test Task", "description": "Task description"}, follow_redirects=False)
    assert create_response.status_code == 302
    # Get dashboard and check for the created task
    dashboard_response = client.get("/dashboard")
    assert b"Test Task" in dashboard_response.content

def test_sync_tasks_endpoint():
    # Simulate a sync request with offline tasks data
    tasks = [{"title": "Offline Task", "description": "Saved offline", "completed": False}]
    response = client.post("/sync_tasks", json={"tasks": tasks})
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"
