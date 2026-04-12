"""Async file-handling utilities."""

from __future__ import annotations

import os
import uuid

import aiofiles
from fastapi import UploadFile


async def save_upload_file(upload_file: UploadFile, destination_dir: str) -> str:
    """Save *upload_file* to *destination_dir* and return the full path."""
    os.makedirs(destination_dir, exist_ok=True)
    ext = os.path.splitext(upload_file.filename or "")[1] or ".bin"
    filename = f"{uuid.uuid4()}{ext}"
    dest_path = os.path.join(destination_dir, filename)

    async with aiofiles.open(dest_path, "wb") as out_file:
        content = await upload_file.read()
        await out_file.write(content)

    return dest_path


def delete_file(path: str) -> None:
    """Delete a file if it exists, ignoring errors."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass
