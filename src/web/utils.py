"""Utility functions for web application."""
from pathlib import Path
from typing import Union


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if needed.
    
    Args:
        path: Directory path to ensure
        
    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path