import pytest
from fastapi.testclient import TestClient
from application.main import app

client = TestClient(app)

def test_landing_page():
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Task & Habit Tracker" in response.content

def test_register_form():
    # GET /register
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Create a New Account" in response.content

def test_login_form():
    # GET /login
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.content

# ... etc. for more coverage ...
