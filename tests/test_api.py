"""API integration tests using httpx + pytest-asyncio."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


# ── Health check ───────────────────────────────────────────────────────────────

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── Validators ─────────────────────────────────────────────────────────────────

def test_generate_rejects_short_prompt(client):
    """Prompt shorter than 10 characters should return 422 Unprocessable Entity."""
    response = client.post("/api/v1/generate", json={"prompt": "Hi"})
    assert response.status_code == 422


def test_generate_rejects_missing_prompt(client):
    response = client.post("/api/v1/generate", json={})
    assert response.status_code == 422


# ── Templates list ─────────────────────────────────────────────────────────────

def test_list_templates_returns_list(client):
    response = client.get("/api/v1/templates")
    assert response.status_code == 200
    body = response.json()
    assert "templates" in body
    assert "total" in body
    assert isinstance(body["templates"], list)


# ── Presentation 404 ───────────────────────────────────────────────────────────

def test_get_presentation_not_found(client):
    response = client.get("/api/v1/presentation/nonexistent-id")
    assert response.status_code == 404


# ── Transform requires .pptx ───────────────────────────────────────────────────

def test_transform_rejects_non_pptx(client):
    import io

    response = client.post(
        "/api/v1/transform",
        files={"file": ("test.txt", io.BytesIO(b"not a pptx"), "text/plain")},
    )
    assert response.status_code == 400


def test_upload_template_rejects_non_json(client):
    import io

    response = client.post(
        "/api/v1/upload-template",
        files={"file": ("template.xml", io.BytesIO(b"<xml/>"), "application/xml")},
    )
    assert response.status_code == 400
