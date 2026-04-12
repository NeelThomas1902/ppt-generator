"""Input validation helpers."""

from __future__ import annotations

from fastapi import HTTPException, UploadFile, status

_ALLOWED_PPTX_CONTENT_TYPES = {
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.ms-powerpoint",
}

_MAX_FILENAME_LENGTH = 255


def validate_pptx_file(file: UploadFile) -> None:
    """Raise an HTTP 400 error if *file* is not a valid .pptx upload."""
    filename = file.filename or ""

    if not filename.lower().endswith(".pptx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .pptx files are accepted.",
        )

    if len(filename) > _MAX_FILENAME_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Filename must not exceed {_MAX_FILENAME_LENGTH} characters.",
        )

    if (
        file.content_type
        and file.content_type not in _ALLOWED_PPTX_CONTENT_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported content type: {file.content_type}",
        )


def validate_prompt(prompt: str, max_length: int = 4000) -> None:
    """Raise a ValueError if *prompt* is empty or too long."""
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must not be empty.")
    if len(prompt) > max_length:
        raise ValueError(f"Prompt must not exceed {max_length} characters.")
