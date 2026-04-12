"""PowerPoint generation service."""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

from app.api.schemas import PresentationResponse
from app.config import settings
from app.services.llm_service import LLMService


_LAYOUT_TITLE = 0
_LAYOUT_TITLE_CONTENT = 1
_LAYOUT_BLANK = 6


class PPTGenerator:
    """Creates .pptx files from LLM-generated slide content."""

    def __init__(self, llm_service: LLMService) -> None:
        self._llm = llm_service

    async def generate(
        self,
        prompt: str,
        template_id: Optional[str] = None,
        slide_count: int = 8,
        theme: Optional[str] = None,
    ) -> PresentationResponse:
        """Generate a presentation and return metadata."""
        content = await self._llm.generate_presentation_content(
            prompt=prompt,
            slide_count=slide_count,
            theme=theme,
        )

        prs = Presentation()
        self._apply_theme(prs, theme)

        # Title slide
        title_layout = prs.slide_layouts[_LAYOUT_TITLE]
        title_slide = prs.slides.add_slide(title_layout)
        title_slide.shapes.title.text = content.get("title", "Presentation")

        # Content slides
        for slide_data in content.get("slides", []):
            layout = prs.slide_layouts[_LAYOUT_TITLE_CONTENT]
            slide = prs.slides.add_slide(layout)

            if slide.shapes.title:
                slide.shapes.title.text = slide_data.get("title", "")

            body = slide.placeholders[1]
            tf = body.text_frame
            tf.clear()

            for i, bullet in enumerate(slide_data.get("content", [])):
                if i == 0:
                    tf.paragraphs[0].text = bullet
                else:
                    p = tf.add_paragraph()
                    p.text = bullet
                    p.level = 0

            if slide_data.get("notes"):
                notes_slide = slide.notes_slide
                notes_slide.notes_text_frame.text = slide_data["notes"]

        # Persist
        os.makedirs(settings.generated_dir, exist_ok=True)
        filename = f"{uuid.uuid4()}.pptx"
        output_path = os.path.join(settings.generated_dir, filename)
        prs.save(output_path)

        return PresentationResponse(
            id=str(uuid.uuid4()),
            filename=filename,
            download_url=f"/generated/{filename}",
            slide_count=len(prs.slides),
            created_at=datetime.now(timezone.utc).isoformat(),
            prompt=prompt,
        )

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _apply_theme(self, prs: Presentation, theme: Optional[str]) -> None:
        """Apply very basic theme colours to the slide master."""
        if theme == "corporate":
            # Dark blue background for title layouts (cosmetic only)
            pass
        # Default: no changes – use python-pptx built-in defaults
