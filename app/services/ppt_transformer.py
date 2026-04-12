from __future__ import annotations

from pathlib import Path

from pptx import Presentation as PptxPresentation
from pptx.dml.color import RGBColor
from pptx.util import Pt
from sqlalchemy.orm import Session

from app.api.schemas import TransformPresentationRequest
from app.config import settings
from app.models.presentation import Presentation
from app.services.template_service import TemplateService

_STYLE_PRESETS: dict[str, dict] = {
    "dark": {"bg": RGBColor(0x1A, 0x1A, 0x2E), "fg": RGBColor(0xFF, 0xFF, 0xFF)},
    "light": {"bg": RGBColor(0xFF, 0xFF, 0xFF), "fg": RGBColor(0x1A, 0x1A, 0x2E)},
    "corporate": {"bg": RGBColor(0x00, 0x33, 0x66), "fg": RGBColor(0xFF, 0xFF, 0xFF)},
}


class PPTTransformer:
    def __init__(self, db: Session):
        self.db = db
        self.template_svc = TemplateService(db)

    async def transform(
        self, presentation: Presentation, request: TransformPresentationRequest
    ) -> Presentation:
        if not presentation.file_path or not Path(presentation.file_path).exists():
            raise FileNotFoundError("Source presentation file not found")

        prs = PptxPresentation(presentation.file_path)
        style = _STYLE_PRESETS.get(request.style.lower(), _STYLE_PRESETS["light"])
        self._apply_style(prs, style)

        output_dir = Path(settings.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        stem = Path(presentation.file_path).stem
        new_path = str(output_dir / f"{stem}_{request.style}.pptx")
        prs.save(new_path)

        presentation.file_path = new_path
        presentation.status = "transformed"
        self.db.commit()
        self.db.refresh(presentation)
        return presentation

    def _apply_style(self, prs: PptxPresentation, style: dict) -> None:
        bg_color: RGBColor = style["bg"]
        for slide in prs.slides:
            background = slide.background
            fill = background.fill
            fill.solid()
            fill.fore_color.rgb = bg_color
