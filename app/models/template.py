"""SQLAlchemy ORM model for presentation templates."""

from __future__ import annotations

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Template(Base):
    """Persisted template definition."""

    __tablename__ = "templates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    theme: Mapped[str | None] = mapped_column(String(100), nullable=True)
    definition: Mapped[str] = mapped_column(Text, nullable=False)  # JSON blob
    slide_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)
