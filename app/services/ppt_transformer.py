"""PowerPoint transformation service – converts existing files into templates."""

from __future__ import annotations

from typing import Optional

from app.api.schemas import TemplateResponse
from app.services.template_service import TemplateService
from app.services.vision_service import VisionService


class PPTTransformer:
    """Analyses an uploaded .pptx file and saves it as a reusable template."""

    def __init__(self, template_service: TemplateService) -> None:
        self._template_service = template_service
        self._vision = VisionService()

    async def transform(
        self,
        file_path: str,
        name: str,
        description: Optional[str] = None,
    ) -> TemplateResponse:
        """Extract structure from *file_path* and persist it as a template.

        Returns the newly created :class:`TemplateResponse`.
        """
        definition = self._vision.analyse(file_path)
        colors = self._vision.extract_theme_colors(file_path)
        if colors:
            definition["theme_colors"] = colors

        return await self._template_service.create_template(
            name=name,
            definition=definition,
            description=description,
        )
