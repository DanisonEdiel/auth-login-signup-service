from fastapi import status
from fastapi.testclient import TestClient

from app.models.user import User


def test_health_check(client: TestClient):
    """
    Test health check endpoint
    """
    response = client.get("/auth/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok", "service": "auth-login-signup-service"}


def test_signup(client: TestClient, db):
    """
    Test user signup
    """
    # Test successful signup
    user_data = {
        "email": "new@example.com",
        "username": "newuser",
        "password": "password123",
        "full_name": "New User"
    }
    
    response = client.post("/auth/signup", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    
    # Test duplicate email
    response = client.post("/auth/signup", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_login(client: TestClient, test_user: User):
    """
    Test user login
    """
    # Test successful login
    login_data = {
        "username": "test@example.com",  # FastAPI OAuth2 uses 'username' field
        "password": "password123"
    }
    
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Test invalid credentials
    login_data["password"] = "wrongpassword"
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
