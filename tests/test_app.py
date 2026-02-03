import copy
import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activities after each test to keep isolation."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Club" in data


def test_successful_signup_adds_participant():
    email = "test1@mergington.edu"
    activity = "Soccer Club"
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert resp.status_code == 200
    data = resp.json()
    assert "Signed up" in data.get("message", "")

    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_duplicate_signup_returns_400():
    email = "duplicate@mergington.edu"
    activity = "Art Club"

    # First signup should succeed
    r1 = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert r1.status_code == 200

    # Second signup should fail with 400 and proper message
    r2 = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert r2.status_code == 400
    assert r2.json().get("detail") == "Student already registered for this activity"


def test_activity_full_returns_400():
    # Create a tiny activity with max_participants=1 for testing
    name = "Tiny Class"
    app_module.activities[name] = {
        "description": "Tiny",
        "schedule": "Now",
        "max_participants": 1,
        "participants": [],
    }

    r1 = client.post(f"/activities/{urllib.parse.quote(name)}/signup?email={urllib.parse.quote('a@x')}")
    assert r1.status_code == 200

    r2 = client.post(f"/activities/{urllib.parse.quote(name)}/signup?email={urllib.parse.quote('b@x')}")
    assert r2.status_code == 400
    assert r2.json().get("detail") == "Activity is full"
