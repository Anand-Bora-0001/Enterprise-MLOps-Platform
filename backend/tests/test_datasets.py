import os
from fastapi.testclient import TestClient

def get_auth_token(client: TestClient) -> str:
    # Use distinct email for tests
    try:
        client.post(
            "/api/v1/auth/signup",
            json={"email": "dataset@example.com", "password": "password", "full_name": "DS User"}
        )
    except:
        pass
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "dataset@example.com", "password": "password"}
    )
    return response.json()["access_token"]

def get_project_id(client: TestClient, token: str) -> int:
    response = client.post(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "DS Project"}
    )
    return response.json()["id"]

def test_upload_dataset(client: TestClient):
    token = get_auth_token(client)
    project_id = get_project_id(client, token)
    
    # Create a dummy CSV file
    file_content = b"col1,col2\n1,2\n3,4"
    files = {'file': ('test.csv', file_content, 'text/csv')}
    data = {'project_id': project_id, 'description': 'Test dataset'}
    
    response = client.post(
        "/api/v1/datasets/upload",
        headers={"Authorization": f"Bearer {token}"},
        data=data,
        files=files
    )
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["name"] == "test.csv"
    assert res_data["format"] == "csv"
    assert "file_path" in res_data
