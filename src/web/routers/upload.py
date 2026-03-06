import shutil
import os
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

SUPPORTED_FORMATS = {'.epub', '.mobi', '.txt'}
UPLOAD_DIR = Path("uploads")

def _save_upload_file(file: UploadFile):
    """Helper function to save an uploaded file"""
    if not file.filename:
        return None

    filename: str = file.filename
    file_ext = Path(filename).suffix.lower()
    if file_ext not in SUPPORTED_FORMATS:
        return None

    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}{file_ext}"

    UPLOAD_DIR.mkdir(exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    return {
        "file_id": file_id,
        "file_path": str(file_path),
        "file_name": filename,
        "file_size": file_size,
        "file_type": file_ext[1:]
    }

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a single file"""
    result = _save_upload_file(file)
    if result is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )
    return result

@router.post("/upload-batch")
async def upload_batch(files: list[UploadFile] = File(...)):
    """Upload multiple files"""
    results = []
    for file in files:
        result = _save_upload_file(file)
        if result:
            results.append(result)
    return {"files": results}
