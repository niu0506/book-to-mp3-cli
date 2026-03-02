import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_test_files_exist():
    """Test that all test files exist"""
    test_dir = Path(__file__).parent
    
    test_files = [
        "test_parsers.py",
        "test_tts_engine.py",
        "test_audio_processor.py",
        "test_batch_processor.py",
        "test_cli.py",
    ]
    
    for test_file in test_files:
        test_path = test_dir / test_file
        assert test_path.exists(), f"{test_file} should exist"

def test_tests_package_exists():
    """Test that tests package exists"""
    tests_path = Path(__file__).parent
    assert tests_path.exists(), "tests package directory should exist"
    assert (tests_path / "__init__.py").exists(), "tests/__init__.py should exist"
