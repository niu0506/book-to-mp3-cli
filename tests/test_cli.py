import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_cli_test_exists():
    """Test that cli test file exists"""
    test_path = Path(__file__).parent / "test_cli.py"
    assert test_path.exists(), "test_cli.py should exist"

def test_all_cli_tests_exist():
    """Test that all CLI test files exist"""
    test_dir = Path(__file__).parent
    
    cli_tests = [
        "test_parsers.py",
        "test_tts_engine.py",
        "test_audio_processor.py",
        "test_batch_processor.py",
        "test_cli.py",
    ]
    
    for test_file in cli_tests:
        test_path = test_dir / test_file
        assert test_path.exists(), f"{test_file} should exist"

def test_all_tests_importable():
    """Test that all test modules can be imported"""
    import tests.test_parsers
    import tests.test_tts_engine
    import tests.test_audio_processor
    import tests.test_batch_processor
    import tests.test_cli
