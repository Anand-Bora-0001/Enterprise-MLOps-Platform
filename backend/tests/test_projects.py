from fastapi.testclient import TestClient

def get_auth_token(client: TestClient) -> str:
    client.post(
        "/api/v1/auth/signup",
        json={"email": "proj@example.com", "password": "password", "full_name": "Proj User"}
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "proj@example.com", "password": "password"}
    )
    return response.json()["access_token"]

def test_create_project(client: TestClient):
    token = get_auth_token(client)
    response = client.post(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Project", "description": "A test project"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert "id" in data

def test_read_projects(client: TestClient):
    token = get_auth_token(client)
    # Create project first
    client.post(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Project 2"}
    )
    
    response = client.get(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] in ["Test Project", "Test Project 2"]
