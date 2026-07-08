from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "test@example.com", "password": "password123", "full_name": "Test User"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login(client: TestClient):
    # First create
    client.post(
        "/api/v1/auth/signup",
        json={"email": "login@example.com", "password": "password123", "full_name": "Login User"}
    )
    
    # Then login
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_users_me(client: TestClient):
    # Setup
    client.post(
        "/api/v1/auth/signup",
        json={"email": "me@example.com", "password": "password123", "full_name": "Me User"}
    )
    login_response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "me@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Fetch Me
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
