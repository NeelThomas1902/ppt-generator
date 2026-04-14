"""PowerPoint transformation service – converts existing files into templates."""

from __future__ import annotations

import os
import shutil
import uuid
from typing import Optional

from app.api.schemas import TemplateResponse
from app.config import settings
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

        template_path = self._store_template_file(file_path)
        if template_path:
            definition["template_file"] = template_path

        return await self._template_service.create_template(
            name=name,
            definition=definition,
            description=description,
        )

    def _store_template_file(self, file_path: str) -> Optional[str]:
        _, ext = os.path.splitext(file_path)
        if not ext:
            return None
        os.makedirs(settings.templates_dir, exist_ok=True)
        filename = f"{uuid.uuid4()}{ext}"
        dest_path = os.path.join(settings.templates_dir, filename)
        shutil.copyfile(file_path, dest_path)
        return dest_path
