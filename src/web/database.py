import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator

DATABASE_PATH = Path("data") / "database.db"
TABLE_NAME = "tasks"

def get_db() -> sqlite3.Connection:
    """Get database connection"""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db_cursor() -> Iterator[sqlite3.Cursor]:
    """Context manager for database cursor"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db() -> None:
    """Initialize database with schema"""
    with get_db_cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id TEXT PRIMARY KEY,
                file_name TEXT NOT NULL,
                original_name TEXT,
                file_type TEXT NOT NULL,
                file_size INTEGER,
                voice TEXT NOT NULL,
                bitrate TEXT NOT NULL,
                segment_length INTEGER NOT NULL,
                status TEXT NOT NULL,
                progress INTEGER DEFAULT 0,
                current_segment INTEGER DEFAULT 0,
                total_segments INTEGER DEFAULT 0,
                output_file TEXT,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
