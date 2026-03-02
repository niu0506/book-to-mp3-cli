import pytest
import sys
from pathlib import Path

test_dir = Path(__file__).parent
project_root = test_dir.parent
src_dir = project_root / "src"

def test_tts_engine_module_exists():
    """Test that tts_engine module exists"""
    tts_engine_path = src_dir / "tts_engine.py"
    assert tts_engine_path.exists(), "tts_engine.py should exist"

def test_audio_processor_module_exists():
    """Test that audio_processor module exists"""
    audio_processor_path = src_dir / "audio_processor.py"
    assert audio_processor_path.exists(), "audio_processor.py should exist"

def test_batch_processor_module_exists():
    """Test that batch_processor module exists"""
    batch_processor_path = src_dir / "batch_processor.py"
    assert batch_processor_path.exists(), "batch_processor.py should exist"

def test_converter_module_exists():
    """Test that converter module exists"""
    converter_path = src_dir / "converter.py"
    assert converter_path.exists(), "converter.py should exist"

def test_cli_module_exists():
    """Test that cli module exists"""
    cli_path = src_dir / "cli.py"
    assert cli_path.exists(), "cli.py should exist"

def test_main_package_exists():
    """Test that main package exists"""
    assert src_dir.exists(), "src package directory should exist"
    assert (src_dir / "__init__.py").exists(), "src/__init__.py should exist"

def test_import_tts_engine():
    """Test that tts_engine can be imported"""
    from src import tts_engine
    assert tts_engine is not None

def test_import_audio_processor():
    """Test that audio_processor can be imported"""
    from src import audio_processor
    assert audio_processor is not None

def test_import_batch_processor():
    """Test that batch_processor can be imported"""
    from src import batch_processor
    assert batch_processor is not None

def test_import_converter():
    """Test that converter can be imported"""
    from src import converter
    assert converter is not None

def test_import_cli():
    """Test that cli can be imported"""
    from src import cli
    assert cli is not None
