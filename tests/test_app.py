from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange: No special setup needed as activities are predefined

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status and that activities are returned
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success():
    # Arrange: Choose an activity and email not already signed up
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check success and that email is now in participants
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]

    # Verify in activities
    response = client.get("/activities")
    data = response.json()
    assert email in data[activity_name]["participants"]


def test_signup_duplicate():
    # Arrange: Sign up first time
    activity_name = "Programming Class"
    email = "dupstudent@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act: Try to sign up again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should fail with 400
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]


def test_signup_activity_not_found():
    # Arrange: Use non-existent activity
    activity_name = "NonExistent Activity"
    email = "test@mergington.edu"

    # Act: Make POST request
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 404
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_delete_success():
    # Arrange: Sign up first
    activity_name = "Gym Class"
    email = "deleteme@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check success and that email is removed
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]

    # Verify removal
    response = client.get("/activities")
    data = response.json()
    assert email not in data[activity_name]["participants"]


def test_delete_not_signed_up():
    # Arrange: Use email not signed up
    activity_name = "Chess Club"
    email = "notsigned@mergington.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should fail with 400
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"]


def test_delete_activity_not_found():
    # Arrange: Use non-existent activity
    activity_name = "NonExistent Activity"
    email = "test@mergington.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 404
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]