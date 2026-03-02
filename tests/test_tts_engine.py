import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tts_engine import TtsEngine
from src.audio_processor import AudioProcessor
from src.batch_processor import BatchProcessor
from src.converter import Converter
from src.cli import main
from src.parsers import ParserFactory

def test_tts_engine_initialization():
    """Test TtsEngine initialization with default and custom parameters"""
    engine = TtsEngine()
    assert engine.voice == "zh-CN-XiaoxiaoNeural"
    assert engine.rate == "+0%"

    engine_custom = TtsEngine(voice="zh-CN-YunxiNeural", rate="+5%")
    assert engine_custom.voice == "zh-CN-YunxiNeural"
    assert engine_custom.rate == "+5%"

def test_tts_engine_text_to_speech_method_exists():
    """Test that text_to_speech method exists"""
    engine = TtsEngine()
    assert hasattr(engine, 'text_to_speech')
    assert callable(engine.text_to_speech)

def test_audio_processor_initialization():
    """Test AudioProcessor initialization"""
    processor = AudioProcessor()
    assert processor.bitrate == '192k'
    assert processor.silence_duration == 3000

def test_audio_processor_split_text():
    """Test text splitting by length"""
    processor = AudioProcessor()
    text = "This is a test text that should be split into segments."
    segments = processor.split_text_by_length(text, segment_length=10)
    assert len(segments) == 6
    assert len(segments[0]) <= 10
    assert len(segments[-1]) <= 10

def test_batch_processor_initialization():
    """Test BatchProcessor initialization"""
    processor = BatchProcessor(workers=2)
    assert processor.workers == 2
    assert processor.converter is not None

def test_batch_processor_invalid_workers():
    """Test BatchProcessor with invalid workers parameter"""
    with pytest.raises(ValueError, match="Workers must be positive"):
        BatchProcessor(workers=0)

def test_converter_initialization():
    """Test Converter initialization"""
    converter = Converter()
    assert converter.voice == "zh-CN-XiaoxiaoNeural"
    assert converter.bitrate == '192k'
    assert converter.segment_length == 500

def test_converter_initialization_with_custom_params():
    """Test Converter with custom parameters"""
    converter = Converter(
        voice="zh-CN-YunxiNeural",
        bitrate='256k',
        segment_length=300
    )
    assert converter.voice == "zh-CN-YunxiNeural"
    assert converter.bitrate == '256k'
    assert converter.segment_length == 300

def test_cli_main_function_exists():
    """Test that main function exists"""
    assert callable(main)

def test_parser_factory_txt():
    """Test ParserFactory with .txt extension"""
    parser = ParserFactory.get_parser('.txt')
    assert parser is not None
    assert hasattr(parser, 'parse')
    assert hasattr(parser, 'supported_formats')

def test_parser_factory_epub():
    """Test ParserFactory with .epub extension"""
    parser = ParserFactory.get_parser('.epub')
    assert parser is not None
    assert hasattr(parser, 'parse')
    assert hasattr(parser, 'supported_formats')

def test_parser_factory_mobi():
    """Test ParserFactory with .mobi extension"""
    parser = ParserFactory.get_parser('.mobi')
    assert parser is not None
    assert hasattr(parser, 'parse')
    assert hasattr(parser, 'supported_formats')

def test_parser_factory_invalid_extension():
    """Test ParserFactory with invalid extension"""
    with pytest.raises(ValueError, match="Unsupported file format"):
        ParserFactory.get_parser('.pdf')
