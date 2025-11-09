from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import IncidentStatus, IncidentSource

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_incident(client):
    response = client.post(
        "/api/incidents",
        json={
            "description": "Test incident",
            "source": "operator",
            "status": "new"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Test incident"
    assert data["source"] == "operator"
    assert data["status"] == "new"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_list_incidents(client):
    # Create a test incident first
    client.post(
        "/api/incidents",
        json={
            "description": "Test incident",
            "source": "monitoring",
            "status": "new"
        }
    )
    
    response = client.get("/api/incidents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)
    assert data[0]["source"] == "monitoring"

def test_update_incident_status(client):
    # Create a test incident
    create_response = client.post(
        "/api/incidents",
        json={
            "description": "Test incident",
            "source": "partner",
            "status": "new"
        }
    )
    incident_id = create_response.json()["id"]
    
    # Update its status
    response = client.patch(
        f"/api/incidents/{incident_id}",
        json={"status": "resolved"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "resolved"

def test_update_nonexistent_incident(client):
    response = client.patch(
        "/api/incidents/999",
        json={"status": "resolved"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"

def test_list_incidents_with_status_filter(client):
    # Create incidents with different statuses
    client.post(
        "/api/incidents",
        json={
            "description": "New incident",
            "source": "operator",
            "status": "new"
        }
    )
    client.post(
        "/api/incidents",
        json={
            "description": "Resolved incident",
            "source": "operator",
            "status": "resolved"
        }
    )
    
    response = client.get("/api/incidents?status=new")
    assert response.status_code == 200
    data = response.json()
    assert all(item["status"] == "new" for item in data)