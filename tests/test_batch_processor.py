import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_batch_processor_test_exists():
    """Test that batch_processor test file exists"""
    test_path = Path(__file__).parent / "test_batch_processor.py"
    assert test_path.exists(), "test_batch_processor.py should exist"

def test_cli_test_exists():
    """Test that cli test file exists"""
    test_path = Path(__file__).parent / "test_cli.py"
    assert test_path.exists(), "test_cli.py should exist"

def test_all_test_files_exist():
    """Test that all test files exist in tests directory"""
    test_dir = Path(__file__).parent
    
    required_files = [
        "__init__.py",
        "test_parsers.py",
        "test_tts_engine.py",
        "test_audio_processor.py",
        "test_batch_processor.py",
        "test_cli.py",
    ]
    
    for file_name in required_files:
        file_path = test_dir / file_name
        assert file_path.exists(), f"{file_name} should exist in tests directory"
        assert file_path.is_file(), f"{file_name} should be a file"
