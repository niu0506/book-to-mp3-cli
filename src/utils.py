"""Utility functions and classes to reduce code redundancy"""

from typing import Callable, Optional
from .config import logger


def call_progress_callback(
    callback: Optional[Callable], 
    progress: float, 
    current_segment: int, 
    total_segments: int,
    current_text_preview: str = ""
):
    """Standardized way to invoke progress callbacks"""
    if callback:
        callback(
            progress=progress,
            current_segment=current_segment,
            total_segments=total_segments,
            current_text_preview=current_text_preview
        )


def safe_file_operation(operation_func, filepath: str, operation_name: str = "file operation"):
    """Safely perform a file operation with error handling"""
    try:
        result = operation_func()
        logger.info(f"Successfully completed {operation_name}: {filepath}")
        return result
    except Exception as e:
        logger.error(f"Error during {operation_name} for {filepath}: {e}")
        raise