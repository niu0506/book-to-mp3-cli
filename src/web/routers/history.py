from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..database import get_db_cursor

router = APIRouter()

OUTPUT_DIR = Path("outputs")

@router.get("/history")
async def get_history():
    """Get conversion history"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT id, file_name, file_type, file_size, voice, bitrate, segment_length,
                   status, progress, created_at, completed_at, output_file
            FROM tasks
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()

    tasks = []
    for row in rows:
        tasks.append({
            "task_id": row["id"],
            "file_name": row["file_name"],
            "file_type": row["file_type"],
            "file_size": row["file_size"],
            "voice": row["voice"],
            "bitrate": row["bitrate"],
            "segment_length": row["segment_length"],
            "status": row["status"],
            "progress": row["progress"],
            "created_at": row["created_at"],
            "completed_at": row["completed_at"],
            "output_file": row["output_file"]
        })

    return {"tasks": tasks}

@router.delete("/history/{task_id}")
async def delete_history(task_id: str):
    """Delete a history record"""
    with get_db_cursor() as cursor:
        # Get task info before deleting
        cursor.execute("SELECT output_file FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Task not found")

        output_file = row["output_file"]

        # Delete from database
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        # Delete output file if exists
        if output_file:
            file_path = Path(output_file)
            if file_path.exists():
                file_path.unlink()

    return {"success": True}

@router.get("/download/{task_id}")
async def download_file(task_id: str):
    """Download converted file"""
    with get_db_cursor() as cursor:
        cursor.execute("SELECT output_file, file_name FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

    if not row or not row["output_file"]:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = Path(row["output_file"])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="audio/mpeg"
    )