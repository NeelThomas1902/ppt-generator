from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Presentation(Base):
    __tablename__ = "presentations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    notes = Column(Text, nullable=True)
