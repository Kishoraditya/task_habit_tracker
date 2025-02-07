import json
import pytest
import requests
from application.utils import store_task_on_ipfs, retrieve_task_from_ipfs


class MockResponse:
    """Mock response object for testing IPFS API."""
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.text = json.dumps(json_data)  # Mocking the text attribute to return a JSON string

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.RequestException("Request failed")


def test_store_task_on_ipfs(monkeypatch):
    """Test storing task data on IPFS."""

    def mock_post(*args, **kwargs):
        """Mock successful IPFS API response."""
        return MockResponse({"Hash": "QmTestHash123456"}, 200)

    monkeypatch.setattr(requests, "post", mock_post)

    dummy_task = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }

    ipfs_hash = store_task_on_ipfs(dummy_task)
    assert isinstance(ipfs_hash, str)
    assert len(ipfs_hash) > 0
    assert ipfs_hash == "QmTestHash123456"


def test_store_task_on_ipfs_failure(monkeypatch):
    """Test failure when IPFS API request fails."""

    def mock_post_fail(*args, **kwargs):
        return MockResponse(None, 500)

    monkeypatch.setattr(requests, "post", mock_post_fail)

    dummy_task = {
        "title": "Fail Task",
        "description": "This is a failed test task",
        "completed": False
    }

    ipfs_hash = store_task_on_ipfs(dummy_task)
    assert ipfs_hash == ""


def test_retrieve_task_from_ipfs(monkeypatch):
    """Test retrieving task data from IPFS."""

    def mock_get(*args, **kwargs):
        """Mock successful task retrieval from IPFS."""
        task_data = {"title": "Test Task", "description": "This is a test task", "completed": False}
        return MockResponse(task_data, 200)

    monkeypatch.setattr(requests, "get", mock_get)

    ipfs_hash = "QmTestHash123456"
    task_data = retrieve_task_from_ipfs(ipfs_hash)
    assert isinstance(task_data, dict)
    assert task_data["title"] == "Test Task"


def test_retrieve_task_from_ipfs_failure(monkeypatch):
    """Test failure when retrieving from IPFS."""

    def mock_get_fail(*args, **kwargs):
        return MockResponse(None, 404)

    monkeypatch.setattr(requests, "get", mock_get_fail)

    ipfs_hash = "QmInvalidHash"
    task_data = retrieve_task_from_ipfs(ipfs_hash)
    assert task_data is None
