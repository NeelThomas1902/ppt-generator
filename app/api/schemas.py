from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GeneratePresentationRequest(BaseModel):
    topic: str = Field(..., description="Topic for the presentation")
    num_slides: int = Field(default=5, ge=1, le=20, description="Number of slides")
    template_id: Optional[int] = Field(default=None, description="Template ID to use")
    additional_context: Optional[str] = Field(default=None, description="Extra context for generation")


class TransformPresentationRequest(BaseModel):
    style: str = Field(..., description="Target style for transformation")
    template_id: Optional[int] = Field(default=None, description="Template ID to apply")


class TemplateCreate(BaseModel):
    name: str = Field(..., description="Template name")
    description: Optional[str] = Field(default=None)
    config: dict = Field(default_factory=dict, description="Template configuration JSON")


class TemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    config: dict


class PresentationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    file_path: Optional[str]
    status: str
