import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.deps import get_db
from app.models.base import Base
from app.models.user import User
from app.models.portfolio import Portfolio # Required for SQLAlchemy relationship mapping

# In-memory database setup for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # clear rate limits for each test
    from app.api.endpoints.auth import login_attempts
    login_attempts.clear()

def test_signup():
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_signup_duplicate_email():
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password456"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login():
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_incorrect_password():
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_me_protected_route():
    # Attempt to access without token
    response = client.get("/auth/me")
    assert response.status_code == 401
    
    # Sign up and log in
    client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    login_response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Access with token
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login_rate_limiting():
    # Hit login 5 times with bad passwords
    for _ in range(5):
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "wrong"}
        )
        assert response.status_code == 401
        
    # The 6th time should hit 429 Too Many Requests
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "wrong"}
    )
    assert response.status_code == 429
    assert "Too many login attempts" in response.json()["detail"]
