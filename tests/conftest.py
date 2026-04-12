"""Shared pytest fixtures for the ppt-generator test suite."""

from __future__ import annotations

import io
import json
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from pptx import Presentation

from app.main import app


# ── Test client ────────────────────────────────────────────────────────────────

@pytest.fixture()
def client():
    """Synchronous TestClient for the FastAPI application."""
    with TestClient(app) as c:
        yield c


# ── Mock LLM data ──────────────────────────────────────────────────────────────

@pytest.fixture()
def mock_llm_content() -> Dict[str, Any]:
    """Minimal presentation content dict as returned by LLMService."""
    return {
        "title": "Test Presentation",
        "slides": [
            {
                "title": "Introduction",
                "content": ["Point A", "Point B"],
                "notes": "Speaker notes here.",
                "layout": "content",
            },
            {
                "title": "Conclusion",
                "content": ["Summary point"],
                "notes": "",
                "layout": "content",
            },
        ],
    }


# ── Sample template JSON ───────────────────────────────────────────────────────

@pytest.fixture()
def sample_template_dict() -> Dict[str, Any]:
    """A minimal but valid template definition dict."""
    return {
        "name": "Test Template",
        "description": "A template used in tests.",
        "theme": "default",
        "colors": {
            "primary": "2E86AB",
            "background": "FFFFFF",
            "text": "1A1A2E",
        },
        "fonts": {"title": "Calibri", "body": "Calibri"},
        "slides": [
            {"layout": "title", "title": "Title Slide"},
            {"layout": "content", "title": "Content Slide", "content": ["Item 1"]},
        ],
    }


@pytest.fixture()
def sample_template_bytes(sample_template_dict: Dict[str, Any]) -> bytes:
    """JSON-encoded bytes for *sample_template_dict*."""
    return json.dumps(sample_template_dict).encode()


# ── Minimal valid PPTX bytes ───────────────────────────────────────────────────

@pytest.fixture()
def valid_pptx_bytes() -> bytes:
    """Bytes of an empty but structurally valid .pptx file."""
    prs = Presentation()
    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()


# ── Mock LLM service ───────────────────────────────────────────────────────────

@pytest.fixture()
def mock_llm_service(mock_llm_content: Dict[str, Any]):
    """Patch LLMService so no real Anthropic API call is made."""
    with patch(
        "app.services.llm_service.LLMService.generate_presentation_content",
        new_callable=AsyncMock,
        return_value=mock_llm_content,
    ) as mock:
        yield mock
