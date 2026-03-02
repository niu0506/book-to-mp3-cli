import pytest
import sys
import tempfile
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.batch_processor import BatchProcessor

def test_batch_processor_initialization():
    """Test BatchProcessor initialization"""
    processor = BatchProcessor(workers=2)
    assert processor.workers == 2
    assert processor.converter is not None

def test_batch_processor_invalid_workers():
    """Test BatchProcessor with invalid workers parameter"""
    with pytest.raises(ValueError, match="Workers must be positive"):
        BatchProcessor(workers=0)

def test_batch_convert_method_exists():
    """Test that batch_convert method exists"""
    processor = BatchProcessor()
    assert hasattr(processor, 'batch_convert')
    assert callable(processor.batch_convert)

def test_batch_processor_with_single_file():
    """Test BatchProcessor with a single file"""
    processor = BatchProcessor(workers=1)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file
        test_file = os.path.join(temp_dir, 'test.txt')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test content for batch processing.")
        
        # Create an output directory
        output_dir = os.path.join(temp_dir, 'output')
        
        results = processor.batch_convert([test_file], output_dir)
        
        assert len(results) == 1
        assert results[0] is not None
        assert os.path.exists(results[0])

def test_batch_processor_with_multiple_files():
    """Test BatchProcessor with multiple files"""
    processor = BatchProcessor(workers=2)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create multiple test files
        files = []
        for i in range(3):
            test_file = os.path.join(temp_dir, f'test_{i}.txt')
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(f"Test content {i}.")
            files.append(test_file)
        
        # Create an output directory
        output_dir = os.path.join(temp_dir, 'output')
        
        results = processor.batch_convert(files, output_dir)
        
        assert len(results) == 3
        for result in results:
            assert result is not None
            assert os.path.exists(result)

def test_batch_processor_with_unsupported_file():
    """Test BatchProcessor with unsupported file type"""
    processor = BatchProcessor(workers=1)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file with unsupported extension
        test_file = os.path.join(temp_dir, 'test.pdf')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test content.")
        
        # Create an output directory
        output_dir = os.path.join(temp_dir, 'output')
        
        # Should handle the error gracefully
        results = processor.batch_convert([test_file], output_dir)
        
        assert len(results) == 0

def test_batch_processor_output_directory_creation():
    """Test that output directory is created if it doesn't exist"""
    processor = BatchProcessor(workers=1)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, 'test.txt')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test content")
        
        output_dir = os.path.join(temp_dir, 'new_output')
        
        results = processor.batch_convert([test_file], output_dir)
        
        assert len(results) == 1
        assert os.path.exists(results[0])
        assert os.path.isdir(output_dir)
