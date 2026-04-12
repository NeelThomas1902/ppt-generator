"""End-to-end integration tests exercising multiple layers together."""

from __future__ import annotations

import io
import json
from typing import Any, Dict
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


# ── Template lifecycle ─────────────────────────────────────────────────────────

def test_upload_template_then_list(client: TestClient, sample_template_bytes: bytes):
    """Upload a JSON template and verify it appears in the /templates list."""
    upload_resp = client.post(
        "/api/v1/upload-template",
        files={"file": ("my_template.json", io.BytesIO(sample_template_bytes), "application/json")},
    )
    assert upload_resp.status_code == 201, upload_resp.text
    created = upload_resp.json()
    assert created["name"] == "Test Template"
    template_id = created["id"]

    list_resp = client.get("/api/v1/templates")
    assert list_resp.status_code == 200
    body = list_resp.json()
    ids = [t["id"] for t in body["templates"]]
    assert template_id in ids


def test_upload_minimal_template_without_name(client: TestClient):
    """A .json template without an explicit 'name' falls back to the filename."""
    nameless = json.dumps({"slides": [{"layout": "title", "title": "Hello"}]}).encode()
    resp = client.post(
        "/api/v1/upload-template",
        files={"file": ("fallback.json", io.BytesIO(nameless), "application/json")},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    # No 'name' key in JSON → service uses filename stem
    assert "fallback" in body["name"]


# ── Generate presentation ──────────────────────────────────────────────────────

def test_generate_presentation_with_mock_llm(
    client: TestClient,
    mock_llm_service: AsyncMock,
):
    """Generate a presentation end-to-end with a mocked LLM response."""
    resp = client.post(
        "/api/v1/generate",
        json={"prompt": "Introduction to machine learning", "slide_count": 2},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert "id" in body
    assert "filename" in body
    assert body["filename"].endswith(".pptx")
    assert "download_url" in body
    assert body["slide_count"] >= 1
    mock_llm_service.assert_called_once()


def test_generate_presentation_returns_valid_response(
    client: TestClient,
    mock_llm_service: AsyncMock,
):
    """Generate response includes required fields even when not persisted to DB."""
    resp = client.post(
        "/api/v1/generate",
        json={"prompt": "Future of renewable energy", "slide_count": 2},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert "id" in body
    assert body["prompt"] == "Future of renewable energy"
    assert body["filename"].endswith(".pptx")


def test_generate_with_theme(
    client: TestClient,
    mock_llm_service: AsyncMock,
):
    """Passing an optional theme does not break the generate endpoint."""
    resp = client.post(
        "/api/v1/generate",
        json={
            "prompt": "Cloud computing best practices",
            "slide_count": 2,
            "theme": "corporate",
        },
    )
    assert resp.status_code == 201, resp.text


# ── Transform endpoint ─────────────────────────────────────────────────────────

def test_transform_valid_pptx(client: TestClient, valid_pptx_bytes: bytes):
    """Uploading a structurally valid PPTX transforms it into a template."""
    resp = client.post(
        "/api/v1/transform?name=Transformed+Template&description=From+test",
        files={
            "file": (
                "slides.pptx",
                io.BytesIO(valid_pptx_bytes),
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["name"] == "Transformed Template"
    assert "id" in body


# ── Error handling ─────────────────────────────────────────────────────────────

def test_get_nonexistent_presentation_returns_404(client: TestClient):
    """Retrieving a presentation that does not exist returns HTTP 404."""
    resp = client.get("/api/v1/presentation/does-not-exist-at-all")
    assert resp.status_code == 404


def test_generate_llm_failure_returns_500(client: TestClient):
    """When the LLM raises an unexpected error the endpoint returns 500."""
    with patch(
        "app.services.llm_service.LLMService.generate_presentation_content",
        new_callable=AsyncMock,
        side_effect=RuntimeError("LLM unavailable"),
    ):
        resp = client.post(
            "/api/v1/generate",
            json={"prompt": "A prompt that triggers an LLM error"},
        )
    assert resp.status_code == 500
