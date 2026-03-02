import pytest
import sys
import tempfile
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parsers import ParserFactory

def test_txt_parser_initialization():
    """Test TxtParser initialization"""
    parser = ParserFactory.get_parser('.txt')
    assert parser.supported_formats == ['txt']

def test_txt_parser_parse_method_exists():
    """Test that parse method exists"""
    parser = ParserFactory.get_parser('.txt')
    assert hasattr(parser, 'parse')
    assert callable(parser.parse)

def test_epub_parser_initialization():
    """Test EpubParser initialization"""
    parser = ParserFactory.get_parser('.epub')
    assert parser.supported_formats == ['epub']

def test_epub_parser_parse_method_exists():
    """Test that parse method exists"""
    parser = ParserFactory.get_parser('.epub')
    assert hasattr(parser, 'parse')
    assert callable(parser.parse)

def test_mobi_parser_initialization():
    """Test Mobiparser initialization"""
    parser = ParserFactory.get_parser('.mobi')
    assert parser.supported_formats == ['mobi']

def test_mobi_parser_parse_method_exists():
    """Test that parse method exists"""
    parser = ParserFactory.get_parser('.mobi')
    assert hasattr(parser, 'parse')
    assert callable(parser.parse)

def test_txt_parser_with_sample_file():
    """Test TxtParser with a sample TXT file"""
    parser = ParserFactory.get_parser('.txt')
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        test_content = "This is a test file content.\nMultiple lines.\n中文测试"
        f.write(test_content)
        temp_file = f.name

    try:
        text, metadata = parser.parse(temp_file)
        assert text is not None
        assert len(text) > 0
        assert '中文测试' in text
        assert metadata['format'] == 'txt'
        assert metadata['language'] == 'zh-CN'
        assert metadata['total_length'] > 0
        assert 'encoding' in metadata
    finally:
        os.unlink(temp_file)

def test_epub_parser_with_sample_file():
    """Test EpubParser with a sample EPUB file"""
    parser = ParserFactory.get_parser('.epub')
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.epub') as f:
        temp_file = f.name

    try:
        # Try to parse (will fail without actual EPUB content, but test the structure)
        try:
            text, metadata = parser.parse(temp_file)
            assert text is not None
            assert metadata['format'] == 'epub'
            assert metadata['language'] == 'zh-CN'
        except Exception as e:
            # Expected to fail without a valid EPUB file
            assert "bad zip file" in str(e).lower() or "not a valid epub file" in str(e).lower() or "could not open" in str(e).lower()
    finally:
        os.unlink(temp_file)

def test_mobi_parser_with_sample_file():
    """Test Mobiparser with a sample MOBI file"""
    parser = ParserFactory.get_parser('.mobi')
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.mobi') as f:
        temp_file = f.name

    try:
        # Try to parse (will fail without actual MOBI content, but test the structure)
        try:
            text, metadata = parser.parse(temp_file)
            assert text is not None
            assert metadata['format'] == 'mobi'
            assert metadata['language'] == 'zh-CN'
        except Exception as e:
            # Expected to fail without a valid MOBI file or mobi library
            assert ("not a valid mobi file" in str(e).lower() or 
                    "mobi library not installed" in str(e).lower() or 
                    "could not open" in str(e).lower())
    finally:
        os.unlink(temp_file)

def test_txt_parser_empty_file():
    """Test TxtParser with empty file"""
    parser = ParserFactory.get_parser('.txt')
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("")
        temp_file = f.name

    try:
        text, metadata = parser.parse(temp_file)
        assert text == ""
        assert len(text) == 0
        assert metadata['total_length'] == 0
    finally:
        os.unlink(temp_file)
