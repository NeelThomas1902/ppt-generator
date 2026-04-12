"""SQLAlchemy ORM model for generated presentations."""

from __future__ import annotations

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Presentation(Base):
    """Persisted presentation record."""

    __tablename__ = "presentations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    slide_count: Mapped[int] = mapped_column(Integer, default=0)
    prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)
