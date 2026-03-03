import pytest
from pathlib import Path
import tempfile


def test_full_conversion_workflow():
    """测试完整的转换工作流"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # 创建测试文件
        test_file = tmpdir / "test.txt"
        test_file.write_text("测试内容测试内容测试内容", encoding='utf-8')

        # 执行转换
        from src.converter import Converter
        converter = Converter()

        output_file = converter.convert(str(test_file), str(tmpdir / "output"))

        # 验证输出
        assert Path(output_file).exists()
        assert output_file.endswith('.mp3')

        # 验证文件大小
        assert Path(output_file).stat().st_size > 0


def test_batch_conversion_workflow():
    """测试批量转换工作流"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # 创建测试文件
        for i in range(3):
            test_file = tmpdir / f"test{i}.txt"
            test_file.write_text(f"测试内容{i}", encoding='utf-8')

        # 测试批量处理器初始化和文件创建
        from src.batch_processor import BatchProcessor

        batch_processor = BatchProcessor(workers=2)
        assert batch_processor.workers == 2
        assert batch_processor.converter is not None

        # 测试批量转换返回正确的类型
        output_dir = str(tmpdir / "batch_output")
        results = batch_processor.batch_convert(
            [str(tmpdir / "test0.txt"), str(tmpdir / "test1.txt"), str(tmpdir / "test2.txt")],
            output_dir
        )

        # 验证返回的是列表
        assert isinstance(results, list)

        # 验证输出目录被创建
        assert Path(output_dir).exists()


def test_epub_parsing_workflow():
    """测试EPUB解析工作流"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # 创建测试EPUB文件（使用ebooklib）
        from ebooklib import epub

        book = epub.EpubBook()
        book.set_identifier('test123')
        book.set_title('Test Book')
        book.set_language('zh-CN')

        chapter = epub.EpubHtml(title='Test', file_name='chap_1.xhtml', lang='zh-CN')
        chapter.content = '<h1>测试章节</h1><p>测试内容</p>'

        book.add_item(chapter)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        epub_filename = tmpdir / "test.epub"
        epub.write_epub(str(epub_filename), book, {})

        # 执行转换
        from src.converter import Converter
        converter = Converter()

        output_file = converter.convert(str(epub_filename), str(tmpdir / "output"))

        # 验证输出
        assert Path(output_file).exists()
        assert output_file.endswith('.mp3')


def test_encoding_detection_workflow():
    """测试编码检测工作流"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # 创建GBK编码的测试文件
        test_file = tmpdir / "test_gbk.txt"
        test_file.write_bytes("GBK测试内容".encode('gbk'))

        # 执行转换
        from src.converter import Converter
        converter = Converter()

        output_file = converter.convert(str(test_file), str(tmpdir / "output"))

        # 验证输出
        assert Path(output_file).exists()
        assert output_file.endswith('.mp3')


def test_tts_engine_integration():
    """测试TTS引擎集成"""
    from src.tts_engine import TtsEngine

    # 测试不同的语音
    voices = [
        "zh-CN-XiaoxiaoNeural",
        "zh-CN-YunxiNeural",
        "en-US-JennyNeural",
    ]

    for voice in voices:
        engine = TtsEngine(voice=voice)
        assert engine.voice == voice


def test_audio_processor_integration():
    """测试音频处理器集成"""
    from src.audio_processor import AudioProcessor

    # 测试文本分割
    processor = AudioProcessor(bitrate='192k')
    segments = processor.split_text_by_length("测试文本测试文本", segment_length=10)

    assert len(segments) > 0
    assert all(len(segment) <= 10 for segment in segments)


def test_batch_processor_with_unsupported_format():
    """测试批量处理时遇到不支持的格式"""
    from src.batch_processor import BatchProcessor

    processor = BatchProcessor(workers=1)

    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建PDF文件（不支持）
        test_file = Path(tmpdir) / "test.pdf"
        test_file.write_text("Test content")

        # 执行批量转换
        output_dir = str(Path(tmpdir) / "output")
        results = processor.batch_convert([str(test_file)], output_dir)

        # 验证结果（应该返回空列表）
        assert len(results) == 0


def test_cli_command_structure():
    """测试CLI命令结构"""
    import sys
    from io import StringIO

    # 测试 --help命令
    from src.cli import main

    # 测试基本命令结构
    from argparse import Namespace

    # 验证命令存在
    from src.cli import main
    assert hasattr(main, '__call__')


def test_error_handling_workflow():
    """测试错误处理工作流"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # 测试短文本文件（应该生成音频）
        test_file = tmpdir / "short.txt"
        test_file.write_text("测试内容", encoding='utf-8')

        # 执行转换（应该能处理短文本）
        from src.converter import Converter
        converter = Converter()

        output_file = converter.convert(str(test_file), str(tmpdir / "output"))

        # 验证输出（应该生成文件）
        assert Path(output_file).exists()


def test_custom_parameters_workflow():
    """测试自定义参数工作流"""
    from src.converter import Converter
    from src.audio_processor import AudioProcessor
    from src.tts_engine import TtsEngine

    # 测试自定义比特率
    converter = Converter(bitrate='128k')
    assert converter.bitrate == '128k'

    # 测试自定义分段长度
    converter = Converter(segment_length=1000)
    assert converter.segment_length == 1000

    # 测试自定义语音
    converter = Converter(voice="en-US-GuyNeural")
    assert converter.voice == "en-US-GuyNeural"


def test_parallel_processing():
    """测试并行处理能力"""
    from src.batch_processor import BatchProcessor

    # 测试不同的worker数量
    for workers in [1, 2, 4]:
        processor = BatchProcessor(workers=workers)
        assert processor.workers == workers

        # 测试无效worker数量
        with pytest.raises(ValueError, match="Workers must be positive"):
            BatchProcessor(workers=0)

        with pytest.raises(ValueError):
            BatchProcessor(workers=-1)
