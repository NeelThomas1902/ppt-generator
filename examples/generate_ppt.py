"""
Example: Generate a PowerPoint presentation using the PPT Generator API.

This script demonstrates how to:
- Send a text prompt to the /api/v1/generate endpoint
- Optionally specify slide count and theme
- Optionally use a saved template
- Download the generated .pptx file

Requirements:
    pip install requests

Usage:
    python examples/generate_ppt.py
"""

import os
import requests

BASE_URL = os.environ.get("PPT_API_URL", "http://localhost:8000")


def generate_presentation(
    prompt: str,
    slide_count: int = 8,
    theme: str | None = None,
    template_id: str | None = None,
) -> dict:
    """Call the /api/v1/generate endpoint and return the response JSON."""
    payload = {
        "prompt": prompt,
        "slide_count": slide_count,
    }
    if theme:
        payload["theme"] = theme
    if template_id:
        payload["template_id"] = template_id

    response = requests.post(
        f"{BASE_URL}/api/v1/generate",
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def download_presentation(download_url: str, output_path: str) -> None:
    """Download the generated .pptx file to a local path."""
    url = download_url if download_url.startswith("http") else f"{BASE_URL}{download_url}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Saved presentation to: {output_path}")


def main() -> None:
    # --- Step 1: Generate the presentation ---
    print("Generating presentation...")
    result = generate_presentation(
        prompt="Create a 5-slide introduction to machine learning for beginners. "
               "Include slides on: what ML is, types of ML, real-world use cases, "
               "how models are trained, and next steps for learning.",
        slide_count=5,
        theme="default",
    )

    print(f"Presentation ID : {result['id']}")
    print(f"Filename        : {result['filename']}")
    print(f"Slides          : {result['slide_count']}")
    print(f"Created at      : {result['created_at']}")
    print(f"Download URL    : {result['download_url']}")

    # --- Step 2: Download the generated file ---
    output_file = result["filename"]
    download_presentation(result["download_url"], output_file)

    print("\nDone! Open the .pptx file in Microsoft PowerPoint or LibreOffice Impress.")


if __name__ == "__main__":
    main()
