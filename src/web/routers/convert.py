import uuid
import logging
import asyncio
from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional
from pydantic import BaseModel

from ..database import get_db_cursor
from ...converter import Converter
from ...utils import call_progress_callback

router = APIRouter()

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")

logger = logging.getLogger(__name__)

main_event_loop: Optional[asyncio.AbstractEventLoop] = None

def find_file_path(file_id: str) -> Optional[Path]:
    """Find file path by checking multiple extensions"""
    for ext in ['.epub', '.mobi', '.txt']:
        test_path = UPLOAD_DIR / f"{file_id}{ext}"
        if test_path.exists():
            return test_path
    return None

def set_main_event_loop(loop: asyncio.AbstractEventLoop) -> None:
    """Store the main event loop reference for background tasks"""
    global main_event_loop
    main_event_loop = loop

def send_websocket_message(task_id: str, message: dict) -> None:
    """Send WebSocket message from background thread"""
    if task_id not in active_tasks or main_event_loop is None:
        return
    for connection in active_tasks[task_id]:
        try:
            asyncio.run_coroutine_threadsafe(
                connection.send_json(message),
                main_event_loop
            )
        except (ConnectionError, RuntimeError) as e:
            logger.warning(f"Failed to send WebSocket message for task {task_id}: {e}")

def create_task_record(task_id: str, file_path: Path, original_name: str, voice: str, bitrate: str, segment_length: int) -> None:
    """Insert task record into database"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO tasks (id, file_name, original_name, file_type, file_size, voice, bitrate, segment_length, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_id,
            file_path.name,
            original_name,
            file_path.suffix[1:],
            file_path.stat().st_size,
            voice,
            bitrate,
            segment_length,
            'pending'
        ))

# In-memory task tracking for WebSocket connections
active_tasks = {}

class ConvertRequest(BaseModel):
    file_id: str
    original_name: Optional[str] = None
    voice: str
    bitrate: str
    segment_length: int
    output_name: Optional[str] = None

class ConvertBatchRequest(BaseModel):
    file_ids: list[str]
    voice: str
    bitrate: str
    segment_length: int

@router.post("/convert")
async def convert_file(request: ConvertRequest, background_tasks: BackgroundTasks):
    """Start a conversion task"""
    logger.info(f"Convert request: {request}")
    
    # Check if file exists
    file_path = find_file_path(request.file_id)

    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    # Generate task ID
    task_id = str(uuid.uuid4())

    # Create task record
    original_name = request.original_name if request.original_name else file_path.stem
    create_task_record(task_id, file_path, original_name, request.voice, request.bitrate, request.segment_length)

    # Start conversion in background
    background_tasks.add_task(
        background_convert_task,
        task_id,
        str(file_path),
        request.voice,
        request.bitrate,
        request.segment_length,
        request.output_name
    )

    return {"task_id": task_id}

@router.post("/convert-batch")
async def convert_batch(request: ConvertBatchRequest, background_tasks: BackgroundTasks):
    """Start batch conversion tasks"""
    task_ids = []
    for file_id in request.file_ids:
        file_path = find_file_path(file_id)

        if file_path:
            task_id = str(uuid.uuid4())
            task_ids.append(task_id)

            # Create task record
            create_task_record(task_id, file_path, file_path.name, request.voice, request.bitrate, request.segment_length)

            # Start conversion in background
            background_tasks.add_task(
                background_convert_task,
                task_id,
                str(file_path),
                request.voice,
                request.bitrate,
                request.segment_length
            )

    return {"task_ids": task_ids}

def background_convert_task(task_id: str, file_path: str, voice: str, bitrate: str, segment_length: int, output_name: Optional[str] = None):
    """Background task for conversion"""
    from datetime import datetime

    # Update status to processing
    with get_db_cursor() as cursor:
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", ('processing', task_id))

    # Progress callback
    def progress_callback(progress: int, current_segment: int, total_segments: int, current_text_preview: str = ""):
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE tasks
                SET progress = ?, current_segment = ?, total_segments = ?
                WHERE id = ?
            """, (int(progress), current_segment, total_segments, task_id))

        message = {
            "type": "progress",
            "progress": int(progress),
            "current_segment": current_segment,
            "total_segments": total_segments,
            "current_text_preview": current_text_preview
        }
        send_websocket_message(task_id, message)
        
        # Additional callback logic specific to web processing could be added here
        # call additional web-specific callbacks if needed

    try:
        # Get original filename from database, fallback to output_name or uuid
        with get_db_cursor() as cursor:
            cursor.execute("SELECT file_name, original_name, output_file FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row and row['original_name']:
                original_name = row['original_name']
            elif output_name:
                original_name = output_name.rsplit('.', 1)[0] if output_name else 'output'
            else:
                original_name = row['file_name'].rsplit('.', 1)[0] if row else Path(file_path).stem

        # Create converter with progress callback
        converter = Converter(
            voice=voice,
            bitrate=bitrate,
            segment_length=segment_length,
            progress_callback=progress_callback
        )

        # Generate output filename from original file name
        output_filename = f"{original_name}.mp3"
        output_file = converter.convert(file_path, str(OUTPUT_DIR), output_filename)

        # Update task as completed
        file_size = Path(output_file).stat().st_size if Path(output_file).exists() else 0
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE tasks
                SET status = ?, progress = 100, output_file = ?, completed_at = ?
                WHERE id = ?
            """, ('completed', output_file, datetime.now().isoformat(), task_id))

        # Notify completion via WebSocket
        message = {
            "type": "complete",
            "output_file": output_file,
            "file_size": file_size
        }
        send_websocket_message(task_id, message)

    except Exception as e:
        # Update task as failed
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE tasks
                SET status = ?, error_message = ?
                WHERE id = ?
            """, ('failed', str(e), task_id))

        # Notify error via WebSocket
        message = {
            "type": "error",
            "error": str(e)
        }
        send_websocket_message(task_id, message)
