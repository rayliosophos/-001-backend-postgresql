import re
import logging
import aiofiles
from uuid import uuid4
from typing import List
from pathlib import Path
from fastapi.responses import FileResponse
from app.api.v1.deps import require_permissions
from app.utils.response_handler import ResponseHandler
from fastapi import APIRouter, Depends, File, UploadFile

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/utility", tags=["Utility"])

MAX_SIZE_MB = 5
UPLOAD_DIR = Path("static/uploads")
ALLOWED_TYPES = {"image/jpeg", "image/png"}
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROFILE_DIR = Path("static/profiles").resolve()
SAFE_FILENAME = re.compile(r"^[a-zA-Z0-9._-]+$")

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

@router.get("/files/profile/{filename}", dependencies=[Depends(require_permissions(["frontend-files:read"]))])
async def get_profile_image(filename: str):
    if not SAFE_FILENAME.match(filename):
        return ResponseHandler.generate_response_unsuccessful(400, "Invalid filename")
    file_path = (PROFILE_DIR / filename).resolve()
    if not str(file_path).startswith(str(PROFILE_DIR)):
        return ResponseHandler.generate_response_unsuccessful(403, "Access denied")
    if not file_path.exists():
        return ResponseHandler.generate_response_unsuccessful(404, "File not found")
    return FileResponse(path=file_path, media_type="application/octet-stream", filename=filename)