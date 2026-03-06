from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .convert import active_tasks

router = APIRouter()

@router.websocket("/progress/{task_id}")
async def websocket_progress(websocket: WebSocket, task_id: str):
    """WebSocket endpoint for real-time progress updates"""
    await websocket.accept()

    # Send initial connection confirmation
    await websocket.send_json({"type": "connected", "task_id": task_id})

    # Register connection
    if task_id not in active_tasks:
        active_tasks[task_id] = []
    active_tasks[task_id].append(websocket)

    try:
        # Keep connection alive
        while True:
            # Wait for messages (client can send heartbeat)
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Remove connection on disconnect
        if task_id in active_tasks and websocket in active_tasks[task_id]:
            active_tasks[task_id].remove(websocket)

        # Clean up if no more connections
        if task_id in active_tasks and not active_tasks[task_id]:
            del active_tasks[task_id]
    except Exception as e:
        print(f"WebSocket error: {e}")
        # Remove connection on error
        if task_id in active_tasks and websocket in active_tasks[task_id]:
            active_tasks[task_id].remove(websocket)