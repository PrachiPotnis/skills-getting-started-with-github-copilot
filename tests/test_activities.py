import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Art Club",
            "Drama Club",
            "Math League",
            "Debate Team"
        ]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activity_keys = list(response.json().keys())
        assert len(activity_keys) == 9
        for activity in expected_activities:
            assert activity in activity_keys


class TestSignup:
    """Tests for POST /activities/{activity}/signup endpoint."""
    
    def test_signup_success(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "new_student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    
    def test_signup_activity_not_found(self, client, reset_activities):
        # Arrange
        activity_name = "NonExistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_student_already_enrolled(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already enrolled
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            headers={"Content-Type": "application/json"}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_adds_participant_to_list(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "test_participant@mergington.edu"
        
        # Act - Sign up
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Act - Get updated activities
        response = client.get("/activities")
        
        # Assert
        participants = response.json()[activity_name]["participants"]
        assert email in participants


class TestUnregister:
    """Tests for DELETE /activities/{activity}/unregister endpoint."""
    
    def test_unregister_success(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already enrolled
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
    
    def test_unregister_activity_not_found(self, client, reset_activities):
        # Arrange
        activity_name = "NonExistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_student_not_enrolled(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "not_enrolled@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_removes_participant(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act - Unregister
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Act - Get updated activities
        response = client.get("/activities")
        
        # Assert
        participants = response.json()[activity_name]["participants"]
        assert email not in participants
