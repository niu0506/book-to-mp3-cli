import pytest
import sys
import tempfile
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.converter import Converter

def test_converter_initialization():
    """Test Converter initialization"""
    converter = Converter()
    assert converter.voice == "zh-CN-XiaoxiaoNeural"
    assert converter.bitrate == '192k'
    assert converter.segment_length == 500

def test_converter_convert_method_exists():
    """Test that convert method exists"""
    converter = Converter()
    assert hasattr(converter, 'convert')
    assert callable(converter.convert)

def test_converter_with_txt_file():
    """Test Converter with a TXT file"""
    converter = Converter()
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, 'test.txt')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("This is a test text content for conversion.")
        
        output_file = converter.convert(test_file, temp_dir)
        
        assert output_file is not None
        assert os.path.exists(output_file)
        assert output_file.endswith('.mp3')

def test_converter_with_multiple_files():
    """Test Converter with a larger text file"""
    converter = Converter()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a larger text file
        test_file = os.path.join(temp_dir, 'test.txt')
        long_text = "This is a test. " * 100
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(long_text)
        
        output_file = converter.convert(test_file, temp_dir)
        
        assert output_file is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0

def test_converter_with_custom_parameters():
    """Test Converter with custom parameters"""
    converter = Converter(
        voice="zh-CN-YunxiNeural",
        bitrate='256k',
        segment_length=300
    )
    
    assert converter.voice == "zh-CN-YunxiNeural"
    assert converter.bitrate == '256k'
    assert converter.segment_length == 300

def test_converter_output_directory_creation():
    """Test that output directory is created if it doesn't exist"""
    converter = Converter()
    
    # Create a temporary directory that doesn't exist
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, 'test.txt')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test content")
        
        output_dir = os.path.join(temp_dir, 'new_output')
        output_file = converter.convert(test_file, output_dir)
        
        assert os.path.exists(output_file)
        assert os.path.isdir(output_dir)
