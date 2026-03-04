from src.app import activities


def test_signup_new_participant_successful(client):
    # Arrange: new email, existing activity
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Act: signup for activity
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert: verify success and participant added
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]


def test_signup_duplicate_email_returns_400(client):
    # Arrange: email already signed up
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act: attempt duplicate signup
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert: verify error response
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange: activity that doesn't exist
    email = "student@mergington.edu"
    activity = "NonExistent Club"
    
    # Act: signup for invalid activity
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert: verify 404 error
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_at_capacity_returns_400(client):
    # Arrange: activity at max capacity
    activity = "Tennis Club"
    # Tennis Club has max 10, currently 1 participant
    # Add 9 more to fill it
    for i in range(9):
        activities[activity]["participants"].append(f"student{i}@mergington.edu")
    
    # Act: attempt signup when at capacity
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": "overcapacity@mergington.edu"}
    )
    
    # Assert: verify capacity error
    assert response.status_code == 400
    assert "at full capacity" in response.json()["detail"]


def test_signup_updates_participant_count(client):
    # Arrange: verify initial count
    activity = "Programming Class"
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Act: signup new participant
    client.post(
        f"/activities/{activity}/signup",
        params={"email": "newperson@mergington.edu"}
    )
    
    # Assert: verify count increased
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity]["participants"])
    assert updated_count == initial_count + 1
