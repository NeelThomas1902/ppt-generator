"""Template management service."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.template import Template
from app.models.presentation import Presentation
from app.api.schemas import PresentationResponse, TemplateResponse


class TemplateService:
    """CRUD operations for templates and presentations."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    # ── Templates ──────────────────────────────────────────────────────────────

    async def list_templates(self) -> List[TemplateResponse]:
        result = await self._db.execute(select(Template).order_by(Template.created_at.desc()))
        templates = result.scalars().all()
        return [self._template_to_schema(t) for t in templates]

    async def get_template(self, template_id: str) -> Optional[TemplateResponse]:
        result = await self._db.execute(
            select(Template).where(Template.id == template_id)
        )
        template = result.scalar_one_or_none()
        return self._template_to_schema(template) if template else None

    async def get_template_definition(self, template_id: str) -> Optional[Dict[str, Any]]:
        result = await self._db.execute(
            select(Template).where(Template.id == template_id)
        )
        template = result.scalar_one_or_none()
        if not template:
            return None
        return json.loads(template.definition)

    async def create_template(
        self,
        name: str,
        definition: Dict[str, Any],
        description: Optional[str] = None,
        theme: Optional[str] = None,
    ) -> TemplateResponse:
        slide_count = len(definition.get("slides", []))
        template = Template(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            theme=theme,
            definition=json.dumps(definition),
            slide_count=slide_count,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._db.add(template)
        await self._db.commit()
        await self._db.refresh(template)
        return self._template_to_schema(template)

    async def create_from_json(
        self, raw_json: bytes, filename: str
    ) -> TemplateResponse:
        definition = json.loads(raw_json)
        name = definition.get("name") or filename.removesuffix(".json")
        description = definition.get("description")
        theme = definition.get("theme")
        return await self.create_template(name, definition, description, theme)

    # ── Presentations ──────────────────────────────────────────────────────────

    async def save_presentation(
        self,
        filename: str,
        slide_count: int,
        prompt: Optional[str] = None,
    ) -> PresentationResponse:
        presentation_id = str(uuid.uuid4())
        presentation = Presentation(
            id=presentation_id,
            filename=filename,
            slide_count=slide_count,
            prompt=prompt,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._db.add(presentation)
        await self._db.commit()
        await self._db.refresh(presentation)
        return self._presentation_to_schema(presentation)

    async def get_presentation(
        self, presentation_id: str
    ) -> Optional[PresentationResponse]:
        result = await self._db.execute(
            select(Presentation).where(Presentation.id == presentation_id)
        )
        presentation = result.scalar_one_or_none()
        return self._presentation_to_schema(presentation) if presentation else None

    # ── Helpers ────────────────────────────────────────────────────────────────

    @staticmethod
    def _template_to_schema(t: Template) -> TemplateResponse:
        return TemplateResponse(
            id=t.id,
            name=t.name,
            description=t.description,
            theme=t.theme,
            slide_count=t.slide_count,
            created_at=t.created_at,
        )

    @staticmethod
    def _presentation_to_schema(p: Presentation) -> PresentationResponse:
        return PresentationResponse(
            id=p.id,
            filename=p.filename,
            download_url=f"/generated/{p.filename}",
            slide_count=p.slide_count,
            created_at=p.created_at,
            prompt=p.prompt,
        )
