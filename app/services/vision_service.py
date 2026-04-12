from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

import anthropic

from app.config import settings


class VisionService:
    """Use Claude's vision capability to analyse slide images."""

    MODEL = "claude-3-5-sonnet-20241022"

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def analyse_slide_image(self, image_path: str) -> dict[str, Any]:
        """Analyse a slide image and return a description dict."""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        media_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        with open(path, "rb") as fh:
            image_data = base64.standard_b64encode(fh.read()).decode("utf-8")

        message = self.client.messages.create(
            model=self.MODEL,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Describe the slide layout, colours, fonts, and content. "
                                "Return a JSON object with keys: layout, colors, fonts, content_summary."
                            ),
                        },
                    ],
                }
            ],
        )

        import json
        import re

        raw = message.content[0].text
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"content_summary": raw}
