def test_get_activities_returns_all_activities(client):
    # Arrange: client is ready
    # Act: fetch activities
    response = client.get("/activities")
    
    # Assert: verify response
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_includes_participant_list(client):
    # Arrange: expecting participant details
    # Act: fetch activities
    response = client.get("/activities")
    data = response.json()
    
    # Assert: verify structure and participants
    chess = data["Chess Club"]
    assert "participants" in chess
    assert "michael@mergington.edu" in chess["participants"]
    assert len(chess["participants"]) == 2


def test_get_activities_includes_max_participants(client):
    # Arrange: activities with capacity limits
    # Act: fetch activities
    response = client.get("/activities")
    data = response.json()
    
    # Assert: verify max_participants field
    assert data["Chess Club"]["max_participants"] == 12
    assert data["Programming Class"]["max_participants"] == 20
