from __future__ import annotations

from typing import Any

import anthropic

from app.config import settings


class LLMService:
    """Wrapper around Anthropic Claude for slide content generation."""

    MODEL = "claude-3-5-sonnet-20241022"

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def generate_slide_content(self, topic: str, num_slides: int, additional_context: str = "") -> list[dict[str, Any]]:
        """Return a list of slide dicts with 'title' and 'content' keys."""
        system_prompt = (
            "You are a professional presentation designer. "
            "Generate structured slide content as a JSON array. "
            "Each element must have 'title' (string) and 'content' (list of bullet strings)."
        )
        user_message = f"Create {num_slides} slides about: {topic}."
        if additional_context:
            user_message += f" Additional context: {additional_context}"

        message = self.client.messages.create(
            model=self.MODEL,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        import json
        import re

        raw = message.content[0].text
        # Extract JSON array from response
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return [{"title": f"Slide {i + 1}", "content": [topic]} for i in range(num_slides)]
