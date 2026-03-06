import asyncio
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from .utils import ensure_directory
from .routers import upload, convert, history, websocket
from .database import init_db
from .routers.convert import set_main_event_loop

app = FastAPI(title="Book to MP3 Converter")

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates_dir = Path(__file__).parent / "templates"

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(convert.router, prefix="/api", tags=["convert"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(templates_dir / "index.html", encoding="utf-8") as f:
        return f.read()

@app.on_event("startup")
async def startup_event():
    ensure_directory("uploads")
    ensure_directory("outputs")
    ensure_directory("data")
    init_db()
    loop = asyncio.get_running_loop()
    set_main_event_loop(loop)

def main():
    uvicorn.run(
        "src.web.main:app",
        host="0.0.0.0",
        port=5000,
        reload=False
    )

if __name__ == "__main__":
    main()