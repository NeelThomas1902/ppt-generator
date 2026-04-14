"""Ollama LLM service for local Qwen models."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import httpx

from app.config import settings


_SYSTEM_PROMPT = """You are an expert presentation designer. When asked to create a presentation,
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


class OllamaLLMService:
    """LLM service backed by a local Ollama server."""

    def __init__(self) -> None:
        self._base_url = settings.ollama_base_url.rstrip("/")
        self._model = settings.ollama_model
        self._timeout = settings.ollama_timeout_seconds

    async def generate_presentation_content(
        self,
        prompt: str,
        slide_count: int = 8,
        theme: Optional[str] = None,
    ) -> Dict[str, Any]:
        user_message = f"Create a {slide_count}-slide presentation about: {prompt}."
        if theme:
            user_message += f" Use a {theme} visual tone."

        content = await self._chat(
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            format_json=True,
        )

        return json.loads(content)

    async def improve_slide_content(
        self,
        slide_content: Dict[str, Any],
        instructions: str,
    ) -> Dict[str, Any]:
        user_message = (
            f"Improve this slide JSON according to the instructions: {instructions}\n\n"
            f"Slide: {json.dumps(slide_content)}\n\n"
            "Return only the updated slide JSON."
        )

        content = await self._chat(
            messages=[{"role": "user", "content": user_message}],
            format_json=True,
        )

        return json.loads(content)

    async def _chat(self, messages: List[Dict[str, str]], format_json: bool) -> str:
        payload: Dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "stream": False,
        }
        if format_json:
            payload["format"] = "json"

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/api/chat",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        return data.get("message", {}).get("content", "")
