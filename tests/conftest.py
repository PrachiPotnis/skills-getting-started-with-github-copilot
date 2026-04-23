import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for API testing."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to a known state before and after each test."""
    # Store original state
    original = {k: {"participants": v["participants"].copy()} for k, v in activities.items()}
    
    yield
    
    # Restore original state after test
    for activity_name, data in activities.items():
        activities[activity_name]["participants"] = original[activity_name]["participants"].copy()
