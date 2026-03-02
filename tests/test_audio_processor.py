import pytest
import sys
import tempfile
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio_processor import AudioProcessor

def test_audio_processor_initialization():
    """Test AudioProcessor initialization"""
    processor = AudioProcessor()
    assert processor.bitrate == '192k'
    assert processor.silence_duration == 3000

def test_audio_processor_initialization_with_custom_bitrate():
    """Test AudioProcessor initialization with custom bitrate"""
    processor = AudioProcessor(bitrate='256k')
    assert processor.bitrate == '256k'
    assert processor.silence_duration == 3000

def test_split_text_by_length_basic():
    """Test basic text splitting"""
    processor = AudioProcessor()
    text = "Hello World"
    segments = processor.split_text_by_length(text, segment_length=5)
    assert len(segments) == 2
    assert segments[0] == "Hello"
    assert segments[1] == "World"

def test_split_text_by_length_exact():
    """Test text splitting when text length is exactly divisible"""
    processor = AudioProcessor()
    text = "12345"
    segments = processor.split_text_by_length(text, segment_length=5)
    assert len(segments) == 1
    assert segments[0] == "12345"

def test_split_text_by_length_longer():
    """Test text splitting with longer segments"""
    processor = AudioProcessor()
    text = "This is a longer text that needs to be split into multiple segments."
    segments = processor.split_text_by_length(text, segment_length=20)
    assert len(segments) == 3

def test_split_text_by_length_zero():
    """Test text splitting with zero segment length"""
    processor = AudioProcessor()
    text = "Test text"
    segments = processor.split_text_by_length(text, segment_length=0)
    assert len(segments) == 1

def test_split_text_by_length_large_segment():
    """Test text splitting with large segment length"""
    processor = AudioProcessor()
    text = "Short text"
    segments = processor.split_text_by_length(text, segment_length=100)
    assert len(segments) == 1

def test_split_empty_text():
    """Test splitting empty text"""
    processor = AudioProcessor()
    segments = processor.split_text_by_length("", segment_length=100)
    assert len(segments) == 1
    assert segments[0] == ""

def test_split_text_with_unicode():
    """Test text splitting with unicode characters"""
    processor = AudioProcessor()
    text = "Hello 你好 世界"
    segments = processor.split_text_by_length(text, segment_length=5)
    assert len(segments) == 2

def test_merge_audio_method_exists():
    """Test that merge_audio method exists"""
    processor = AudioProcessor()
    assert hasattr(processor, 'merge_audio')
    assert callable(processor.merge_audio)
