from __future__ import annotations

import os
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.schemas import (
    GeneratePresentationRequest,
    PresentationResponse,
    TemplateCreate,
    TemplateResponse,
    TransformPresentationRequest,
)
from app.database import get_db
from app.models.presentation import Presentation
from app.models.template import Template
from app.services.ppt_generator import PPTGenerator
from app.services.ppt_transformer import PPTTransformer
from app.services.template_service import TemplateService

router = APIRouter()


# ── Templates ────────────────────────────────────────────────────────────────

@router.post("/templates", response_model=TemplateResponse, status_code=201)
def create_template(payload: TemplateCreate, db: Session = Depends(get_db)):
    svc = TemplateService(db)
    return svc.create_template(payload)


@router.get("/templates", response_model=list[TemplateResponse])
def list_templates(db: Session = Depends(get_db)):
    svc = TemplateService(db)
    return svc.list_templates()


@router.get("/templates/{template_id}", response_model=TemplateResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    svc = TemplateService(db)
    template = svc.get_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.delete("/templates/{template_id}", status_code=204)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    svc = TemplateService(db)
    if not svc.delete_template(template_id):
        raise HTTPException(status_code=404, detail="Template not found")


# ── Presentations ─────────────────────────────────────────────────────────────

@router.post("/presentations/generate", response_model=PresentationResponse, status_code=201)
async def generate_presentation(
    payload: GeneratePresentationRequest,
    db: Session = Depends(get_db),
):
    generator = PPTGenerator(db)
    try:
        presentation = await generator.generate(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return presentation


@router.post("/presentations/transform/{presentation_id}", response_model=PresentationResponse)
async def transform_presentation(
    presentation_id: int,
    payload: TransformPresentationRequest,
    db: Session = Depends(get_db),
):
    transformer = PPTTransformer(db)
    presentation = db.query(Presentation).get(presentation_id)
    if presentation is None:
        raise HTTPException(status_code=404, detail="Presentation not found")
    try:
        updated = await transformer.transform(presentation, payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return updated


@router.post("/presentations/upload", response_model=PresentationResponse, status_code=201)
async def upload_presentation(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    from app.utils.file_handlers import save_upload
    from app.utils.validators import validate_pptx

    if not validate_pptx(file.filename):
        raise HTTPException(status_code=400, detail="Only .pptx files are accepted")

    file_path = await save_upload(file)
    presentation = Presentation(
        title=file.filename,
        file_path=file_path,
        status="uploaded",
    )
    db.add(presentation)
    db.commit()
    db.refresh(presentation)
    return presentation


@router.get("/presentations/{presentation_id}/download")
def download_presentation(presentation_id: int, db: Session = Depends(get_db)):
    presentation = db.query(Presentation).get(presentation_id)
    if presentation is None or not presentation.file_path:
        raise HTTPException(status_code=404, detail="Presentation not found")
    if not os.path.exists(presentation.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    return FileResponse(
        presentation.file_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=os.path.basename(presentation.file_path),
    )


@router.get("/presentations", response_model=list[PresentationResponse])
def list_presentations(db: Session = Depends(get_db)):
    return db.query(Presentation).all()


@router.get("/presentations/{presentation_id}", response_model=PresentationResponse)
def get_presentation(presentation_id: int, db: Session = Depends(get_db)):
    presentation = db.query(Presentation).get(presentation_id)
    if presentation is None:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return presentation
