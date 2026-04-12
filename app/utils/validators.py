from __future__ import annotations

from pathlib import Path


ALLOWED_EXTENSIONS = {".pptx"}
MAX_TOPIC_LENGTH = 500


def validate_pptx(filename: str | None) -> bool:
    """Return True if the filename has a .pptx extension."""
    if not filename:
        return False
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def validate_topic(topic: str) -> bool:
    """Return True if the topic string is non-empty and within length limits."""
    return bool(topic.strip()) and len(topic.strip()) <= MAX_TOPIC_LENGTH
