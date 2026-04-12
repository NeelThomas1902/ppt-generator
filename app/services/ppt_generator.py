from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from pptx import Presentation as PptxPresentation
from pptx.util import Inches, Pt
from sqlalchemy.orm import Session

from app.api.schemas import GeneratePresentationRequest
from app.config import settings
from app.models.presentation import Presentation
from app.services.llm_service import LLMService
from app.services.template_service import TemplateService


class PPTGenerator:
    def __init__(self, db: Session):
        self.db = db
        self.llm = LLMService()
        self.template_svc = TemplateService(db)

    async def generate(self, request: GeneratePresentationRequest) -> Presentation:
        slides_data = self.llm.generate_slide_content(
            topic=request.topic,
            num_slides=request.num_slides,
            additional_context=request.additional_context or "",
        )

        template_config: dict[str, Any] = {}
        if request.template_id is not None:
            tmpl = self.template_svc.get_template(request.template_id)
            if tmpl:
                template_config = tmpl.config

        prs = PptxPresentation()
        self._apply_theme(prs, template_config)

        for slide_data in slides_data:
            self._add_slide(prs, slide_data)

        output_dir = Path(settings.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_title = "".join(c if c.isalnum() else "_" for c in request.topic)[:50]
        file_path = str(output_dir / f"{safe_title}.pptx")
        prs.save(file_path)

        presentation = Presentation(
            title=request.topic,
            file_path=file_path,
            status="ready",
        )
        self.db.add(presentation)
        self.db.commit()
        self.db.refresh(presentation)
        return presentation

    def _apply_theme(self, prs: PptxPresentation, config: dict[str, Any]) -> None:
        if "slide_width" in config:
            prs.slide_width = Inches(config["slide_width"])
        if "slide_height" in config:
            prs.slide_height = Inches(config["slide_height"])

    def _add_slide(self, prs: PptxPresentation, slide_data: dict[str, Any]) -> None:
        layout = prs.slide_layouts[1]  # title + content layout
        slide = prs.slides.add_slide(layout)

        title_shape = slide.shapes.title
        if title_shape:
            title_shape.text = slide_data.get("title", "")

        body = slide.placeholders[1] if len(slide.placeholders) > 1 else None
        if body:
            tf = body.text_frame
            tf.text = ""
            bullets = slide_data.get("content", [])
            if isinstance(bullets, list):
                for i, bullet in enumerate(bullets):
                    if i == 0:
                        tf.text = str(bullet)
                    else:
                        p = tf.add_paragraph()
                        p.text = str(bullet)
            elif isinstance(bullets, str):
                tf.text = bullets
