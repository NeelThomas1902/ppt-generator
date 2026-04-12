from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models import template, presentation  # noqa: F401 - register models with Base
from app.main import app

# In-memory SQLite for tests — StaticPool ensures all connections share one database
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_create_and_list_templates():
    payload = {"name": "test_tmpl", "description": "A test template", "config": {"slide_width": 10}}
    response = client.post("/api/v1/templates", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test_tmpl"

    list_response = client.get("/api/v1/templates")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_get_template_not_found():
    response = client.get("/api/v1/templates/9999")
    assert response.status_code == 404


def test_delete_template():
    payload = {"name": "to_delete", "config": {}}
    create_resp = client.post("/api/v1/templates", json=payload)
    template_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/templates/{template_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/api/v1/templates/{template_id}")
    assert get_resp.status_code == 404


def test_list_presentations_empty():
    response = client.get("/api/v1/presentations")
    assert response.status_code == 200
    assert response.json() == []


def test_upload_invalid_extension(tmp_path):
    fake_file = tmp_path / "test.txt"
    fake_file.write_text("not a pptx")
    with open(fake_file, "rb") as fh:
        response = client.post(
            "/api/v1/presentations/upload",
            files={"file": ("test.txt", fh, "text/plain")},
        )
    assert response.status_code == 400
