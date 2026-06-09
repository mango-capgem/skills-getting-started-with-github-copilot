def test_get_activities_returns_expected_payload(client):
    # Arrange

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()
    updated_activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in updated_activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_remove_participant_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    payload = response.json()
    updated_activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Removed {email} from {activity_name}"
    assert email not in updated_activities[activity_name]["participants"]


def test_remove_participant_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_remove_participant_returns_400_for_not_registered_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student is not signed up for this activity"
