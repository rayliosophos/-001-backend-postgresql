import logging
import aiofiles
from uuid import uuid4
from typing import List
from pathlib import Path

from fastapi.responses import FileResponse
from app.utils.response_handler import ResponseHandler
from fastapi import APIRouter, Depends, File, UploadFile
from app.dependencies.require_permission_dep import require_permissions

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/utility", tags=["Utility"])

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_TYPES = {"image/jpeg", "image/png"}
MAX_SIZE_MB = 5

@router.post("/upload",dependencies=[Depends(require_permissions(["frontend-files:write"]))])
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        if file.content_type not in ALLOWED_TYPES:
            return ResponseHandler.generate_response_unsuccessful(400, f"Invalid file type: {file.filename}")
        contents = await file.read()
        if len(contents) > MAX_SIZE_MB * 1024 * 1024:
            return ResponseHandler.generate_response_unsuccessful(400, f"File too large: {file.filename}")
        file_ext = Path(file.filename).suffix
        stored_name = f"{uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / stored_name
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(contents)
        uploaded_files.append({
            "original_name": file.filename,
            "stored_name": stored_name,
            "content_type": file.content_type,
            "size": f"{round(len(contents) / (1024 * 1024), 2)} MB"
        })

    return ResponseHandler.generate_response_successful("Files uploaded successfully", uploaded_files)

@router.get("/files/profile/{filename}",dependencies=[Depends(require_permissions(["frontend-files:read"]))])
async def get_profile_image(
    filename: str
):
    file_path = Path("static/profiles") / filename

    if not file_path.exists():
        return ResponseHandler.generate_response_unsuccessful(404, "File not found")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=filename
    )