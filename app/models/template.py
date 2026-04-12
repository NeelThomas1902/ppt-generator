from __future__ import annotations

from sqlalchemy import JSON, Column, Integer, String, Text

from app.database import Base


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    config = Column(JSON, nullable=False, default=dict)
