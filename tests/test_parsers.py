import pytest
import os
import sys
from pathlib import Path

test_dir = Path(__file__).parent
project_root = test_dir.parent
src_dir = project_root / "src"
parsers_dir = src_dir / "parsers"

def test_epub_parser_module_exists():
    """Test that epub_parser module exists"""
    epub_parser_path = parsers_dir / "epub_parser.py"
    assert epub_parser_path.exists(), "epub_parser.py should exist"

def test_mobi_parser_module_exists():
    """Test that mobi_parser module exists"""
    mobi_parser_path = parsers_dir / "mobi_parser.py"
    assert mobi_parser_path.exists(), "mobi_parser.py should exist"

def test_txt_parser_module_exists():
    """Test that txt_parser module exists"""
    txt_parser_path = parsers_dir / "txt_parser.py"
    assert txt_parser_path.exists(), "txt_parser.py should exist"

def test_parsers_package_exists():
    """Test that parsers package exists"""
    assert parsers_dir.exists(), "parsers package directory should exist"
    assert (parsers_dir / "__init__.py").exists(), "parsers/__init__.py should exist"

def test_import_epub_parser():
    """Test that epub_parser can be imported"""
    from src.parsers import epub_parser
    assert epub_parser is not None

def test_import_mobi_parser():
    """Test that mobi_parser can be imported"""
    from src.parsers import mobi_parser
    assert mobi_parser is not None

def test_import_txt_parser():
    """Test that txt_parser can be imported"""
    from src.parsers import txt_parser
    assert txt_parser is not None
