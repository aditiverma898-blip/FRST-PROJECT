import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from api.app import app, app_state

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_dataset():
    # Provide a dummy dataset for tests
    app_state["df"] = pd.DataFrame({
        "restaurant_name": ["Test Cafe", "Spicy Place"],
        "city": ["Delhi", "Mumbai"],
        "cuisines": ["Italian, Cafe", "Indian"],
        "cost_for_two": [800.0, 400.0],
        "aggregate_rating": [4.5, 3.8],
        "votes": [320, 150],
        "budget_category": ["medium", "low"],
        "has_online_delivery": [True, False],
        "has_table_booking": [False, True]
    })
    yield
    app_state["df"] = None

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["dataset_loaded"] is True

def test_get_locations():
    response = client.get("/api/v1/locations")
    assert response.status_code == 200
    assert response.json() == ["Delhi", "Mumbai"]

def test_get_cuisines():
    response = client.get("/api/v1/cuisines")
    assert response.status_code == 200
    # Should split 'Italian, Cafe' into ['Italian', 'Cafe'] and sort
    assert set(response.json()) == {"Cafe", "Indian", "Italian"}

@patch("api.routes.llm_client.get_recommendation")
def test_recommend(mock_generate):
    mock_generate.return_value = '''
    [
        {
            "rank": 1,
            "restaurant_name": "Test Cafe",
            "cuisine": "Italian",
            "rating": 4.5,
            "cost_for_two": 800,
            "explanation": "Great vibe."
        }
    ]
    '''
    
    payload = {
        "location": "Delhi",
        "budget": "medium",
        "cuisines": ["Italian"],
        "min_rating": 4.0,
        "vibe": "chill"
    }
    
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] == 1
    assert len(data["recommendations"]) == 1
    assert data["recommendations"][0]["name"] == "Test Cafe"
