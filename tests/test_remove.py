def test_remove_participant_successful(client):
    # Arrange: participant exists
    activity = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act: remove participant
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert: verify success
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    assert email in response.json()["message"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange: email not signed up
    activity = "Chess Club"
    email = "nosuchstudent@mergington.edu"
    
    # Act: attempt to remove non-signed-up email
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert: verify 404 error
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"]


def test_remove_from_nonexistent_activity_returns_404(client):
    # Arrange: activity doesn't exist
    activity = "Fake Activity"
    email = "student@mergington.edu"
    
    # Act: attempt to remove from invalid activity
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert: verify 404 error
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_updates_participant_list(client):
    # Arrange: verify participant in list
    activity = "Chess Club"
    email = "michael@mergington.edu"
    response_before = client.get("/activities")
    assert email in response_before.json()[activity]["participants"]
    
    # Act: remove participant
    client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert: verify removed from list
    response_after = client.get("/activities")
    assert email not in response_after.json()[activity]["participants"]
