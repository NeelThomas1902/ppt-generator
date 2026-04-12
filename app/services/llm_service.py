"""Claude LLM service for generating presentation content."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import anthropic

from app.config import settings


SYSTEM_PROMPT = """You are an expert presentation designer. When asked to create a presentation,
you respond ONLY with a valid JSON object following this exact schema:

{
  "title": "Presentation title",
  "slides": [
    {
      "title": "Slide title",
      "content": ["Bullet point 1", "Bullet point 2"],
      "notes": "Optional speaker notes",
      "layout": "title|content|two_column|blank"
    }
  ]
}

No markdown, no explanation – just the JSON."""


class LLMService:
    """Thin wrapper around the Anthropic client."""

    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def generate_presentation_content(
        self,
        prompt: str,
        slide_count: int = 8,
        theme: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Ask Claude to produce structured slide content for a presentation.

        Returns a dict with ``title`` and ``slides`` keys.
        """
        user_message = (
            f"Create a {slide_count}-slide presentation about: {prompt}."
        )
        if theme:
            user_message += f" Use a {theme} visual tone."

        message = self._client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        raw = message.content[0].text
        return json.loads(raw)

    async def improve_slide_content(
        self,
        slide_content: Dict[str, Any],
        instructions: str,
    ) -> Dict[str, Any]:
        """Rewrite a single slide according to additional instructions."""
        user_message = (
            f"Improve this slide JSON according to the instructions: {instructions}\n\n"
            f"Slide: {json.dumps(slide_content)}\n\n"
            "Return only the updated slide JSON."
        )

        message = self._client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_message}],
        )

        raw = message.content[0].text
        return json.loads(raw)
