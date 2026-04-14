"""Shared LLM client protocol for provider implementations."""

from __future__ import annotations

from typing import Any, Dict, Optional, Protocol


class LLMClient(Protocol):
    """Protocol for LLM services used by the PPT generator."""

    async def generate_presentation_content(
        self,
        prompt: str,
        slide_count: int = 8,
        theme: Optional[str] = None,
    ) -> Dict[str, Any]:
        ...

    async def improve_slide_content(
        self,
        slide_content: Dict[str, Any],
        instructions: str,
    ) -> Dict[str, Any]:
        ...
