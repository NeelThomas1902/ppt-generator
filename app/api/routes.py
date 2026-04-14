"""API route definitions."""

from __future__ import annotations

import logging
import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import (
    GenerateRequest,
    PresentationResponse,
    TemplateListResponse,
    TemplateResponse,
    TransformRequest,
)
from app.config import settings
from app.database import get_db
from app.services.llm_service import LLMService
from app.services.llm_service_mock import MockLLMService
from app.services.llm_service_ollama import OllamaLLMService
from app.services.llm_types import LLMClient
from app.services.ppt_generator import PPTGenerator
from app.services.ppt_transformer import PPTTransformer
from app.services.template_service import TemplateService
from app.utils.file_handlers import save_upload_file
from app.utils.validators import validate_pptx_file

router = APIRouter()
logger = logging.getLogger(__name__)


# ── Dependency helpers ─────────────────────────────────────────────────────────

def get_llm_service() -> LLMClient:
    if settings.demo_mode:
        return MockLLMService()
    if settings.llm_provider.lower() == "ollama":
        return OllamaLLMService()
    return LLMService()


def get_ppt_generator(llm: LLMClient = Depends(get_llm_service)) -> PPTGenerator:
    return PPTGenerator(llm)


def get_template_service(db: AsyncSession = Depends(get_db)) -> TemplateService:
    return TemplateService(db)


def get_ppt_transformer(
    template_service: TemplateService = Depends(get_template_service),
) -> PPTTransformer:
    return PPTTransformer(template_service)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post(
    "/generate",
    response_model=PresentationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a PPT from a text prompt",
)
async def generate_presentation(
    request: GenerateRequest,
    generator: PPTGenerator = Depends(get_ppt_generator),
    template_service: TemplateService = Depends(get_template_service),
):
    """Generate a PowerPoint presentation from a natural-language prompt."""
    try:
        template_definition = None
        if request.template_id:
            template_definition = await template_service.get_template_definition(
                request.template_id
            )
            if not template_definition:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Template '{request.template_id}' not found.",
                )
        presentation = await generator.generate(
            prompt=request.prompt,
            template_id=request.template_id,
            slide_count=request.slide_count,
            theme=request.theme,
            template_definition=template_definition,
        )
        return presentation
    except Exception as exc:
        if isinstance(exc, HTTPException):
            raise
        logger.exception("Generate failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate presentation. Please try again.",
        ) from exc


@router.post(
    "/transform",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Convert an uploaded PPT file into a reusable template",
)
async def transform_presentation(
    file: UploadFile = File(...),
    name: str = "",
    description: str = "",
    transformer: PPTTransformer = Depends(get_ppt_transformer),
):
    """Upload an existing PowerPoint file and convert it to a template."""
    validate_pptx_file(file)
    saved_path = await save_upload_file(file, settings.upload_dir)
    try:
        template = await transformer.transform(
            file_path=saved_path,
            name=name or file.filename or "Untitled",
            description=description or None,
        )
        return template
    finally:
        if os.path.exists(saved_path):
            os.remove(saved_path)


@router.post(
    "/upload-template",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a JSON template definition",
)
async def upload_template(
    file: UploadFile = File(...),
    template_service: TemplateService = Depends(get_template_service),
):
    """Upload a JSON file that defines a presentation template."""
    if not file.filename or not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .json template files are accepted.",
        )
    content = await file.read()
    template = await template_service.create_from_json(content, file.filename)
    return template


@router.get(
    "/templates",
    response_model=TemplateListResponse,
    summary="List all available templates",
)
async def list_templates(
    template_service: TemplateService = Depends(get_template_service),
):
    """Return all stored presentation templates."""
    templates = await template_service.list_templates()
    return TemplateListResponse(templates=templates, total=len(templates))


@router.get(
    "/presentation/{presentation_id}",
    response_model=PresentationResponse,
    summary="Retrieve a generated presentation by ID",
)
async def get_presentation(
    presentation_id: str,
    template_service: TemplateService = Depends(get_template_service),
):
    """Fetch metadata and download link for a previously generated presentation."""
    presentation = await template_service.get_presentation(presentation_id)
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Presentation '{presentation_id}' not found.",
        )
    return presentation
