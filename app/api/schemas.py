"""Pydantic schemas for request and response validation."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ── Request schemas ────────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    """Request body for generating a new presentation."""

    prompt: str = Field(..., min_length=10, description="Text prompt describing the presentation content.")
    template_id: Optional[str] = Field(None, description="ID of a saved template to use.")
    slide_count: int = Field(default=8, ge=1, le=50, description="Number of slides to generate.")
    theme: Optional[str] = Field(None, description="Visual theme name (e.g. 'corporate', 'default').")


class TransformRequest(BaseModel):
    """Request body for transforming an uploaded PPT into a reusable template."""

    name: str = Field(..., min_length=1, description="Name for the new template.")
    description: Optional[str] = Field(None, description="Optional description of the template.")


# ── Response schemas ───────────────────────────────────────────────────────────

class TemplateResponse(BaseModel):
    """Information about a stored template."""

    id: str
    name: str
    description: Optional[str] = None
    theme: Optional[str] = None
    slide_count: int
    created_at: str

    model_config = {"from_attributes": True}


class PresentationResponse(BaseModel):
    """Information about a generated presentation."""

    id: str
    filename: str
    download_url: str
    slide_count: int
    created_at: str
    prompt: Optional[str] = None

    model_config = {"from_attributes": True}


class TemplateListResponse(BaseModel):
    """List of templates."""

    templates: List[TemplateResponse]
    total: int


class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str
    code: Optional[str] = None
