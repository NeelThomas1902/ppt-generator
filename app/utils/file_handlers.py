from __future__ import annotations

import os
import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.config import settings


async def save_upload(file: UploadFile) -> str:
    """Persist an uploaded file and return its path."""
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename or "upload.bin").suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest = upload_dir / unique_name

    async with aiofiles.open(dest, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            await out.write(chunk)

    return str(dest)


def delete_file(file_path: str) -> bool:
    """Delete a file from disk. Returns True if deleted, False if not found."""
    try:
        os.remove(file_path)
        return True
    except FileNotFoundError:
        return False
