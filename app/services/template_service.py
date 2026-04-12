from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.api.schemas import TemplateCreate, TemplateResponse
from app.models.template import Template


class TemplateService:
    BUILTIN_DIR = Path(__file__).parent.parent / "templates"

    def __init__(self, db: Session):
        self.db = db

    # ── CRUD ─────────────────────────────────────────────────────────────────

    def create_template(self, payload: TemplateCreate) -> Template:
        template = Template(
            name=payload.name,
            description=payload.description,
            config=payload.config,
        )
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def list_templates(self) -> list[Template]:
        return self.db.query(Template).all()

    def get_template(self, template_id: int) -> Optional[Template]:
        return self.db.get(Template, template_id)

    def delete_template(self, template_id: int) -> bool:
        template = self.get_template(template_id)
        if template is None:
            return False
        self.db.delete(template)
        self.db.commit()
        return True

    # ── Built-in templates ────────────────────────────────────────────────────

    def load_builtin(self, name: str) -> dict[str, Any]:
        file_path = self.BUILTIN_DIR / f"{name}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Built-in template '{name}' not found")
        with open(file_path) as fh:
            return json.load(fh)
