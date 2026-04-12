"""Unit tests for service-layer helpers."""

from __future__ import annotations

import io
import json
import os
import tempfile

import pytest
from fastapi import UploadFile

from app.utils.validators import validate_pptx_file, validate_prompt


# ── validate_prompt ────────────────────────────────────────────────────────────

def test_validate_prompt_raises_on_empty():
    with pytest.raises(ValueError, match="empty"):
        validate_prompt("")


def test_validate_prompt_raises_on_whitespace():
    with pytest.raises(ValueError, match="empty"):
        validate_prompt("   ")


def test_validate_prompt_raises_on_too_long():
    with pytest.raises(ValueError, match="exceed"):
        validate_prompt("a" * 4001)


def test_validate_prompt_passes_valid():
    validate_prompt("Tell me about machine learning in healthcare.")


# ── validate_pptx_file ─────────────────────────────────────────────────────────

def _make_upload(filename: str, content_type: str = "application/octet-stream") -> UploadFile:
    return UploadFile(filename=filename, file=io.BytesIO(b""), headers={"content-type": content_type})


def test_validate_pptx_accepts_valid_file():
    upload = _make_upload(
        "slides.pptx",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
    validate_pptx_file(upload)  # should not raise


def test_validate_pptx_rejects_txt():
    from fastapi import HTTPException

    upload = _make_upload("notes.txt", "text/plain")
    with pytest.raises(HTTPException) as exc_info:
        validate_pptx_file(upload)
    assert exc_info.value.status_code == 400


def test_validate_pptx_rejects_long_filename():
    from fastapi import HTTPException

    upload = _make_upload("a" * 256 + ".pptx")
    with pytest.raises(HTTPException) as exc_info:
        validate_pptx_file(upload)
    assert exc_info.value.status_code == 400


# ── Template JSON loading ──────────────────────────────────────────────────────

def test_default_template_is_valid_json():
    path = os.path.join(
        os.path.dirname(__file__), "..", "app", "templates", "default_template.json"
    )
    with open(path) as f:
        data = json.load(f)
    assert "name" in data
    assert "slides" in data


def test_corporate_theme_is_valid_json():
    path = os.path.join(
        os.path.dirname(__file__), "..", "app", "templates", "corporate_theme.json"
    )
    with open(path) as f:
        data = json.load(f)
    assert "name" in data
    assert "theme" in data
    assert "slides" in data
