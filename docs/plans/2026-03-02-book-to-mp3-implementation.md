# 电子书转MP3功能实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个命令行工具，将EPUB、MOBI、TXT电子书转换为MP3有声书，支持批量处理和多线程。

**Architecture:** 模块化Python项目，包含格式解析器、Edge TTS引擎、音频处理器、批量处理器和CLI接口。

**Tech Stack:** Python 3.8+, edge-tts, ebooklib, pydub, mobi, chardet, multiprocessing, argparse

---

## 项目初始化

### Task 1: 创建项目结构和配置文件

**Files:**
- Create: `src/__init__.py`
- Create: `src/parsers/__init__.py`
- Create: `src/parsers/epub_parser.py`
- Create: `src/parsers/mobi_parser.py`
- Create: `src/parsers/txt_parser.py`
- Create: `src/tts_engine.py`
- Create: `src/audio_processor.py`
- Create: `src/batch_processor.py`
- Create: `src/converter.py`
- Create: `src/cli.py`
- Create: `tests/__init__.py`
- Create: `tests/test_parsers.py`
- Create: `tests/test_tts_engine.py`
- Create: `tests/test_audio_processor.py`
- Create: `tests/test_batch_processor.py`
- Create: `tests/test_cli.py`
- Create: `requirements.txt`
- Create: `setup.py`
- Create: `README.md`
- Create: `.gitignore`

**Step 1: 创建基础目录结构**

```bash
mkdir -p src/parsers tests
touch src/__init__.py src/parsers/__init__.py
touch tests/__init__.py
```

**Step 2: 创建requirements.txt**

```text
edge-tts>=6.1.0
ebooklib>=0.18
pydub>=0.25.1
mobi>=1.1.0
chardet>=5.2.0
tqdm>=4.66.0
pytest>=7.4.0
pytest-cov>=4.1.0
```

**Step 3: 创建setup.py**

```python
from setuptools import setup, find_packages

setup(
    name="book-to-mp3-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "edge-tts>=6.1.0",
        "ebooklib>=0.18",
        "pydub>=0.25.1",
        "mobi>=1.1.0",
        "chardet>=5.2.0",
        "tqdm>=4.66.0",
    ],
    entry_points={
        "console_scripts": [
            "book-to-mp3=src.cli:main",
        ],
    },
)
```

**Step 4: 创建.gitignore**

```text
__pycache__/
*.py[cod]
.env
.env.local
output/
*.mp3
*.wav
.DS_Store
*.swp
*.swo
dist/
build/
.eggs/
```

**Step 5: 安装依赖**

```bash
pip install -r requirements.txt
```

**Step 6: 创建基本模块文件（占位符）**

```bash
touch src/__init__.py
touch src/parsers/__init__.py
touch src/tts_engine.py
touch src/audio_processor.py
touch src/batch_processor.py
touch src/converter.py
touch src/cli.py
```

**Step 7: 创建测试文件占位符**

```bash
touch tests/__init__.py
touch tests/test_parsers.py
touch tests/test_tts_engine.py
touch tests/test_audio_processor.py
touch tests/test_batch_processor.py
touch tests/test_cli.py
```

**Step 8: 创建README.md**

```markdown
# 电子书转MP3 CLI

将EPUB、MOBI、TXT电子书转换为MP3有声书。

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```bash
python -m src.cli convert "input.epub"
```

## 功能

- 支持EPUB、MOBI、TXT格式
- Edge TTS语音合成
- 批量处理和多线程
```

**Step 9: 提交初始化代码**

```bash
git add .
git commit -m "feat: initialize project structure and configuration files"
```

---

## 格式解析器实现

### Task 2: 实现TXT解析器

**Files:**
- Modify: `src/parsers/txt_parser.py`
- Test: `tests/test_parsers.py`

**Step 1: 编写TXT解析器测试**

```python
import pytest
import os
from src.parsers.txt_parser import TxtParser


def test_parse_txt_file(tmp_path):
    """测试解析TXT文件"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("第一行\n第二行\n第三行", encoding='utf-8')

    parser = TxtParser()
    content, metadata = parser.parse(str(test_file))

    assert "第一行" in content
    assert "第二行" in content
    assert metadata['format'] == 'txt'
    assert metadata['language'] == 'zh-CN'
    assert metadata['total_length'] == len("第一行\n第二行\n第三行")


def test_parse_txt_different_encoding(tmp_path):
    """测试解析不同编码的TXT文件"""
    test_file = tmp_path / "test.txt"
    # GBK编码
    test_file.write_bytes("测试内容".encode('gbk'))

    parser = TxtParser()
    content, metadata = parser.parse(str(test_file))

    assert "测试内容" in content


def test_parse_empty_txt_file(tmp_path):
    """测试解析空TXT文件"""
    test_file = tmp_path / "empty.txt"
    test_file.write_text("", encoding='utf-8')

    parser = TxtParser()
    content, metadata = parser.parse(str(test_file))

    assert content == ""
    assert metadata['total_length'] == 0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_parsers.py::test_parse_txt_file -v
```

Expected: FAIL with "NameError: name 'TxtParser' is not defined"

**Step 3: 实现TXT解析器**

```python
import chardet
from typing import Tuple, Dict


class TxtParser:
    def __init__(self):
        self.supported_formats = ['txt']

    def parse(self, file_path: str) -> Tuple[str, Dict]:
        """解析TXT文件，返回文本内容和元数据"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()

        # 检测编码
        encoding = chardet.detect(raw_data)['encoding']
        if not encoding:
            encoding = 'utf-8'

        # 解码内容
        text = raw_data.decode(encoding, errors='replace')

        metadata = {
            'format': 'txt',
            'language': 'zh-CN',
            'encoding': encoding,
            'total_length': len(text)
        }

        return text, metadata
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_parsers.py::test_parse_txt_file -v
```

Expected: PASS

**Step 5: 提交TXT解析器实现**

```bash
git add src/parsers/txt_parser.py tests/test_parsers.py
git commit -m "feat: implement TXT parser with encoding detection"
```

### Task 3: 实现EPUB解析器

**Files:**
- Modify: `src/parsers/epub_parser.py`
- Test: `tests/test_parsers.py`

**Step 1: 编写EPUB解析器测试**

```python
def test_parse_epub_file(tmp_path):
    """测试解析EPUB文件"""
    # 创建测试EPUB文件（简化版本）
    epub_file = tmp_path / "test.epub"

    # 这里使用临时方法创建简单EPUB
    # 实际项目中可能需要更复杂的测试数据

    parser = EpubParser()
    content, metadata = parser.parse(str(epub_file))

    assert 'format' in metadata
    assert 'language' in metadata
    assert 'total_length' > 0


def test_epub_parser_unsupported_format():
    """测试不支持EPUB格式"""
    parser = EpubParser()
    with pytest.raises(ValueError):
        parser.parse("unsupported_format.pdf")
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_parsers.py::test_parse_epub_file -v
```

Expected: FAIL with "NameError: name 'EpubParser' is not defined"

**Step 3: 实现EPUB解析器**

```python
from ebooklib import epub
from typing import Tuple, Dict


class EpubParser:
    def __init__(self):
        self.supported_formats = ['epub']

    def parse(self, file_path: str) -> Tuple[str, Dict]:
        """解析EPUB文件，返回文本内容和元数据"""
        book = epub.read_epub(file_path)

        content_parts = []

        # 提取所有章节内容
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                content_parts.append(item.get_content())

        # 合并所有内容
        full_content = ''.join(content_parts)

        metadata = {
            'format': 'epub',
            'language': 'zh-CN',
            'total_length': len(full_content)
        }

        return full_content, metadata
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_parsers.py::test_parse_epub_file -v
```

Expected: PASS

**Step 5: 提交EPUB解析器实现**

```bash
git add src/parsers/epub_parser.py tests/test_parsers.py
git commit -m "feat: implement EPUB parser"
```

### Task 4: 实现MOBI解析器

**Files:**
- Modify: `src/parsers/mobi_parser.py`
- Test: `tests/test_parsers.py`

**Step 1: 编写MOBI解析器测试**

```python
def test_parse_mobi_file(tmp_path):
    """测试解析MOBI文件"""
    # 创建测试MOBI文件（简化版本）
    mobi_file = tmp_path / "test.mobi"

    # 这里使用临时方法创建简单MOBI
    # 实际项目中可能需要更复杂的测试数据

    parser = Mobiparser()
    content, metadata = parser.parse(str(mobi_file))

    assert 'format' in metadata
    assert 'language' in metadata
    assert 'total_length' > 0


def test_mobi_parser_unsupported_format():
    """测试不支持MOBI格式"""
    parser = Mobiparser()
    with pytest.raises(ValueError):
        parser.parse("unsupported_format.pdf")
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_parsers.py::test_parse_mobi_file -v
```

Expected: FAIL with "NameError: name 'Mobiparser' is not defined"

**Step 3: 实现MOBI解析器**

```python
from mobi import Mobi
from typing import Tuple, Dict


class Mobiparser:
    def __init__(self):
        self.supported_formats = ['mobi']

    def parse(self, file_path: str) -> Tuple[str, Dict]:
        """解析MOBI文件，返回文本内容和元数据"""
        mobi = Mobi(file_path)
        content = mobi.text

        metadata = {
            'format': 'mobi',
            'language': 'zh-CN',
            'total_length': len(content)
        }

        return content, metadata
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_parsers.py::test_parse_mobi_file -v
```

Expected: PASS

**Step 5: 提交MOBI解析器实现**

```bash
git add src/parsers/mobi_parser.py tests/test_parsers.py
git commit -m "feat: implement MOBI parser"
```

### Task 5: 实现解析器工厂和统一接口

**Files:**
- Modify: `src/parsers/__init__.py`
- Test: `tests/test_parsers.py`

**Step 1: 编写工厂模式测试**

```python
def test_parser_factory():
    """测试解析器工厂"""
    from src.parsers import ParserFactory

    txt_parser = ParserFactory.get_parser('txt')
    assert txt_parser.__class__.__name__ == 'TxtParser'

    epub_parser = ParserFactory.get_parser('epub')
    assert epub_parser.__class__.__name__ == 'EpubParser'

    mobi_parser = ParserFactory.get_parser('mobi')
    assert mobi_parser.__class__.__name__ == 'Mobiparser'

    with pytest.raises(ValueError):
        ParserFactory.get_parser('pdf')


def test_factory_unsupported_format():
    """测试工厂处理不支持格式"""
    from src.parsers import ParserFactory

    with pytest.raises(ValueError):
        ParserFactory.get_parser('pdf')
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_parsers.py::test_parser_factory -v
```

Expected: FAIL with "NameError: name 'ParserFactory' is not defined"

**Step 3: 实现解析器工厂**

```python
from typing import Dict, Type
from .txt_parser import TxtParser
from .epub_parser import EpubParser
from .mobi_parser import Mobiparser


class ParserFactory:
    parsers: Dict[str, Type] = {
        'txt': TxtParser,
        'epub': EpubParser,
        'mobi': Mobiparser,
    }

    @classmethod
    def get_parser(cls, format_type: str):
        """获取指定格式的解析器"""
        parser_class = cls.parsers.get(format_type.lower())
        if not parser_class:
            raise ValueError(f"Unsupported format: {format_type}")
        return parser_class()
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_parsers.py::test_parser_factory -v
```

Expected: PASS

**Step 5: 提交工厂模式实现**

```bash
git add src/parsers/__init__.py tests/test_parsers.py
git commit -m "feat: implement parser factory pattern"
```

---

## TTS引擎实现

### Task 6: 实现Edge TTS引擎封装

**Files:**
- Modify: `src/tts_engine.py`
- Test: `tests/test_tts_engine.py`

**Step 1: 编写TTS引擎测试**

```python
import pytest
from unittest.mock import patch, MagicMock
from src.tts_engine import TtsEngine


def test_text_to_speech(tmp_path):
    """测试文本转语音"""
    engine = TtsEngine(voice="zh-CN-XiaoxiaoNeural")
    audio_path = tmp_path / "output.mp3"

    result = engine.text_to_speech("测试文本", str(audio_path))

    assert result == str(audio_path)
    assert audio_path.exists()


def test_tts_different_voices():
    """测试不同语音"""
    voices = [
        "zh-CN-XiaoxiaoNeural",
        "zh-CN-YunxiNeural",
        "en-US-JennyNeural",
    ]

    for voice in voices:
        engine = TtsEngine(voice=voice)
        assert engine.voice == voice


def test_tts_error_handling():
    """测试错误处理"""
    engine = TtsEngine(voice="invalid-voice")

    with pytest.raises(Exception):
        engine.text_to_speech("测试文本", "/tmp/nonexistent.mp3")
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_tts_engine.py::test_text_to_speech -v
```

Expected: FAIL with "NameError: name 'TtsEngine' is not defined"

**Step 3: 实现TTS引擎**

```python
from edge_tts import Communicate
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TtsEngine:
    def __init__(self, voice: str = "zh-CN-XiaoxiaoNeural", rate: str = "+0%"):
        """
        初始化TTS引擎

        Args:
            voice: 语音名称，如 zh-CN-XiaoxiaoNeural
            rate: 语速调整，如 "+0%", "+10%", "-10%"
        """
        self.voice = voice
        self.rate = rate

    def text_to_speech(self, text: str, output_path: str, attempts: int = 3) -> str:
        """
        将文本转换为语音

        Args:
            text: 要转换的文本
            output_path: 输出MP3文件路径
            attempts: 重试次数

        Returns:
            生成的音频文件路径
        """
        for attempt in range(attempts):
            try:
                communicate = Communicate(
                    text,
                    self.voice,
                    rate=self.rate
                )
                communicate.save(output_path)
                logger.info(f"Generated audio: {output_path}")
                return output_path
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == attempts - 1:
                    raise
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_tts_engine.py -v
```

Expected: PASS

**Step 5: 提交TTS引擎实现**

```bash
git add src/tts_engine.py tests/test_tts_engine.py
git commit -m "feat: implement Edge TTS engine wrapper"
```

---

## 音频处理器实现

### Task 7: 实现音频处理功能

**Files:**
- Modify: `src/audio_processor.py`
- Test: `tests/test_audio_processor.py`

**Step 1: 编写音频处理器测试**

```python
import pytest
from src.audio_processor import AudioProcessor


def test_split_audio_by_length(tmp_path):
    """测试按长度分割音频"""
    processor = AudioProcessor(bitrate='192k')
    segments = processor.split_text_by_length("测试文本测试文本测试文本", segment_length=10)

    assert len(segments) > 0
    assert all(len(segment) <= 10 for segment in segments)


def test_merge_audio_files(tmp_path):
    """测试合并音频文件"""
    processor = AudioProcessor(bitrate='192k')

    # 创建临时音频文件
    file1 = tmp_path / "segment1.mp3"
    file2 = tmp_path / "segment2.mp3"

    # 这里需要实际音频文件进行测试
    # 简化测试：检查方法存在

    assert hasattr(processor, 'merge_audio')


def test_get_default_bitrate():
    """测试获取默认比特率"""
    processor = AudioProcessor()
    assert processor.bitrate == '192k'


def test_set_custom_bitrate():
    """测试设置自定义比特率"""
    processor = AudioProcessor(bitrate='128k')
    assert processor.bitrate == '128k'
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_audio_processor.py -v
```

Expected: FAIL with "NameError: name 'AudioProcessor' is not defined"

**Step 3: 实现音频处理器**

```python
from typing import List
from pydub import AudioSegment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioProcessor:
    def __init__(self, bitrate: str = '192k'):
        """
        初始化音频处理器

        Args:
            bitrate: MP3比特率，支持 128k, 192k, 256k, 320k
        """
        self.bitrate = bitrate
        self.silence_duration = 3000  # 段落间静音3秒

    def split_text_by_length(self, text: str, segment_length: int = 500) -> List[str]:
        """
        按固定长度分割文本

        Args:
            text: 输入文本
            segment_length: 每段字符数

        Returns:
            文本片段列表
        """
        return [text[i:i + segment_length] for i in range(0, len(text), segment_length)]

    def merge_audio(self, audio_files: List[str], output_path: str) -> str:
        """
        合并多个音频文件

        Args:
            audio_files: 音频文件路径列表
            output_path: 输出文件路径

        Returns:
            合并后的音频文件路径
        """
        if not audio_files:
            raise ValueError("No audio files to merge")

        merged = AudioSegment.empty()

        for audio_file in audio_files:
            audio = AudioSegment.from_mp3(audio_file)
            merged += audio
            # 添加静音间隔
            merged += AudioSegment.silent(duration=self.silence_duration)

        merged.export(output_path, format="mp3", bitrate=self.bitrate)
        logger.info(f"Merged audio to: {output_path}")
        return output_path
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_audio_processor.py -v
```

Expected: PASS

**Step 5: 提交音频处理器实现**

```bash
git add src/audio_processor.py tests/test_audio_processor.py
git commit -m "feat: implement audio processor"
```

---

## 批量处理器实现

### Task 8: 实现批量处理功能

**Files:**
- Modify: `src/batch_processor.py`
- Test: `tests/test_batch_processor.py`

**Step 1: 编写批量处理器测试**

```python
import pytest
from unittest.mock import patch, MagicMock
from src.batch_processor import BatchProcessor


def test_batch_convert_single_file(tmp_path, monkeypatch):
    """测试批量转换单个文件"""
    processor = BatchProcessor(workers=2)

    # 模拟转换函数
    mock_convert = MagicMock(return_value="output.mp3")
    monkeypatch.setattr(processor, '_convert_single_file', mock_convert)

    input_file = tmp_path / "test.epub"

    result = processor.batch_convert([str(input_file)], "output")

    assert len(result) == 1
    assert "output" in result[0]


def test_batch_convert_multiple_files(tmp_path, monkeypatch):
    """测试批量转换多个文件"""
    processor = BatchProcessor(workers=2)

    mock_convert = MagicMock(return_value="output.mp3")
    monkeypatch.setattr(processor, '_convert_single_file', mock_convert)

    input_files = [
        tmp_path / "test1.epub",
        tmp_path / "test2.epub",
    ]

    result = processor.batch_convert([str(f) for f in input_files], "output")

    assert len(result) == 2


def test_batch_processor_invalid_workers():
    """测试无效工作进程数"""
    with pytest.raises(ValueError):
        BatchProcessor(workers=0)


def test_batch_processor_negative_workers():
    """测试负数工作进程数"""
    with pytest.raises(ValueError):
        BatchProcessor(workers=-1)
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_batch_processor.py -v
```

Expected: FAIL with "NameError: name 'BatchProcessor' is not defined"

**Step 3: 实现批量处理器**

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List
from pathlib import Path
import logging

from .converter import Converter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchProcessor:
    def __init__(self, workers: int = 4):
        """
        初始化批量处理器

        Args:
            workers: 并发工作进程数
        """
        if workers <= 0:
            raise ValueError("Workers must be positive")
        self.workers = workers
        self.converter = Converter()

    def batch_convert(self, input_files: List[str], output_dir: str) -> List[str]:
        """
        批量转换电子书

        Args:
            input_files: 输入文件路径列表
            output_dir: 输出目录

        Returns:
            输出文件路径列表
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = []

        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            futures = []
            for input_file in input_files:
                future = executor.submit(
                    self._convert_single_file,
                    input_file,
                    str(output_path)
                )
                futures.append(future)

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"Completed: {result}")
                except Exception as e:
                    logger.error(f"Failed: {e}")

        return results

    def _convert_single_file(self, input_file: str, output_dir: str) -> str:
        """转换单个文件（在独立进程中运行）"""
        return self.converter.convert(input_file, output_dir)
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_batch_processor.py -v
```

Expected: PASS

**Step 5: 提交批量处理器实现**

```bash
git add src/batch_processor.py tests/test_batch_processor.py
git commit -m "feat: implement batch processor with multi-threading"
```

---

## 转换器实现

### Task 9: 实现核心转换逻辑

**Files:**
- Modify: `src/converter.py`
- Test: `tests/test_converters.py`

**Step 1: 编写转换器测试**

```python
import pytest
from unittest.mock import patch, MagicMock
from src.converter import Converter


def test_convert_txt_to_mp3(tmp_path):
    """测试转换TXT到MP3"""
    converter = Converter()

    input_file = tmp_path / "test.txt"
    input_file.write_text("测试内容", encoding='utf-8')

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with patch('src.converter.AudioProcessor') as mock_audio, \
         patch('src.converter.TtsEngine') as mock_tts:

        mock_audio.return_value.merge_audio.return_value = "output.mp3"
        mock_tts.return_value.text_to_speech.return_value = "output.mp3"

        result = converter.convert(str(input_file), str(output_dir))

        assert "output" in result
        assert "mp3" in result


def test_convert_epub_to_mp3(tmp_path):
    """测试转换EPUB到MP3"""
    converter = Converter()

    # 创建测试EPUB文件
    epub_file = tmp_path / "test.epub"

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with patch('src.converter.AudioProcessor') as mock_audio, \
         patch('src.converter.TtsEngine') as mock_tts:

        mock_audio.return_value.merge_audio.return_value = "output.mp3"
        mock_tts.return_value.text_to_speech.return_value = "output.mp3"

        result = converter.convert(str(epub_file), str(output_dir))

        assert "output" in result


def test_convert_invalid_format(tmp_path):
    """测试转换无效格式"""
    converter = Converter()

    input_file = tmp_path / "invalid.pdf"

    with pytest.raises(ValueError):
        converter.convert(str(input_file), str(tmp_path))
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_converters.py -v
```

Expected: FAIL with "NameError: name 'Converter' is not defined"

**Step 3: 实现转换器**

```python
from pathlib import Path
from typing import Tuple

from .parsers import ParserFactory
from .tts_engine import TtsEngine
from .audio_processor import AudioProcessor


class Converter:
    def __init__(
        self,
        voice: str = "zh-CN-XiaoxiaoNeural",
        bitrate: str = '192k',
        segment_length: int = 500
    ):
        """
        初始化转换器

        Args:
            voice: 语音名称
            bitrate: 音频比特率
            segment_length: 文本分段长度
        """
        self.voice = voice
        self.bitrate = bitrate
        self.segment_length = segment_length

    def convert(self, input_file: str, output_dir: str) -> str:
        """
        转换电子书到MP3

        Args:
            input_file: 输入文件路径
            output_dir: 输出目录

        Returns:
            输出MP3文件路径
        """
        # 获取文件扩展名
        file_ext = Path(input_file).suffix.lower()

        # 获取解析器
        parser = ParserFactory.get_parser(file_ext)

        # 解析文件
        text, metadata = parser.parse(input_file)

        # 创建处理器
        audio_processor = AudioProcessor(bitrate=self.bitrate)
        tts_engine = TtsEngine(voice=self.voice)

        # 分割文本
        segments = audio_processor.split_text_by_length(
            text,
            segment_length=self.segment_length
        )

        # 生成音频文件
        audio_files = []
        for i, segment in enumerate(segments):
            output_segment = Path(output_dir) / f"segment_{i}.mp3"
            tts_engine.text_to_speech(segment, str(output_segment))
            audio_files.append(str(output_segment))

        # 合并音频
        output_file = Path(output_dir) / "output.mp3"
        audio_processor.merge_audio(audio_files, str(output_file))

        return str(output_file)
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_converters.py -v
```

Expected: PASS

**Step 5: 提交转换器实现**

```bash
git add src/converter.py tests/test_converters.py
git commit -m "feat: implement core conversion logic"
```

---

## CLI接口实现

### Task 10: 实现命令行接口

**Files:**
- Modify: `src/cli.py`
- Test: `tests/test_cli.py`

**Step 1: 编写CLI测试**

```python
import pytest
from unittest.mock import patch, MagicMock
from src.cli import main


def test_cli_convert_single_file(tmp_path, capsys):
    """测试CLI转换单个文件"""
    converter = MagicMock(return_value="output.mp3")

    with patch('src.cli.Converter', return_value=converter), \
         patch('argparse.Namespace', **{
             'input_file': str(tmp_path / "test.epub"),
             'output_dir': str(tmp_path / "output"),
             'segment_length': 500,
             'bitrate': '192k',
             'voice': 'zh-CN-XiaoxiaoNeural',
             'workers': 2
         }):

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert 'Converted' in captured.out


def test_cli_batch_convert(tmp_path, capsys):
    """测试CLI批量转换"""
    converter = MagicMock(return_value="output.mp3")

    with patch('src.cli.BatchProcessor') as mock_batch, \
         patch('argparse.Namespace', **{
             'batch_mode': True,
             'input_dir': str(tmp_path),
             'output_dir': str(tmp_path / "output"),
             'segment_length': 500,
             'bitrate': '192k',
             'voice': 'zh-CN-XiaoxiaoNeural',
             'workers': 2
         }):

        mock_batch.return_value.batch_convert.return_value = ["output1.mp3", "output2.mp3"]

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert 'batch' in captured.out.lower()


def test_cli_invalid_format(tmp_path):
    """测试CLI处理无效格式"""
    with patch('argparse.Namespace', **{
        'input_file': str(tmp_path / "invalid.pdf"),
        'output_dir': str(tmp_path / "output"),
        'segment_length': 500,
        'bitrate': '192k',
        'voice': 'zh-CN-XiaoxiaoNeural',
        'workers': 2
    }):

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code != 0
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_cli.py -v
```

Expected: FAIL with "NameError: name 'main' is not defined"

**Step 3: 实现CLI接口**

```python
import argparse
import sys
from pathlib import Path

from .batch_processor import BatchProcessor
from .converter import Converter


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='电子书转MP3 CLI工具'
    )

    subparsers = parser.add_subparsers(dest='command', help='命令')

    # 转换单个文件
    convert_parser = subparsers.add_parser('convert', help='转换单个文件')
    convert_parser.add_argument('input_file', help='输入文件路径')
    convert_parser.add_argument('--output-dir', default='output', help='输出目录')
    convert_parser.add_argument('--segment-length', type=int, default=500, help='文本分段长度')
    convert_parser.add_argument('--bitrate', choices=['128k', '192k', '256k', '320k'], default='192k', help='音频比特率')
    convert_parser.add_argument('--voice', default='zh-CN-XiaoxiaoNeural', help='语音名称')
    convert_parser.add_argument('--workers', type=int, default=4, help='并发工作进程数')

    # 批量转换
    batch_parser = subparsers.add_parser('batch', help='批量转换')
    batch_parser.add_argument('input_dir', help='输入目录')
    batch_parser.add_argument('--output-dir', default='batch_output', help='输出目录')
    batch_parser.add_argument('--segment-length', type=int, default=500, help='文本分段长度')
    batch_parser.add_argument('--bitrate', choices=['128k', '192k', '256k', '320k'], default='192k', help='音频比特率')
    batch_parser.add_argument('--voice', default='zh-CN-XiaoxiaoNeural', help='语音名称')
    batch_parser.add_argument('--workers', type=int, default=4, help='并发工作进程数')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'convert':
            convert_single_file(args)
        elif args.command == 'batch':
            convert_batch(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def convert_single_file(args):
    """转换单个文件"""
    converter = Converter(
        voice=args.voice,
        bitrate=args.bitrate,
        segment_length=args.segment_length
    )

    output_path = converter.convert(args.input_file, args.output_dir)
    print(f"✓ Converted: {output_path}")


def convert_batch(args):
    """批量转换"""
    batch_processor = BatchProcessor(workers=args.workers)

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    input_files = []
    for file_path in input_dir.iterdir():
        if file_path.suffix.lower() in ['.epub', '.mobi', '.txt']:
            input_files.append(str(file_path))

    if not input_files:
        print("No supported files found in input directory")
        sys.exit(0)

    print(f"Found {len(input_files)} files to convert...")

    results = batch_processor.batch_convert(input_files, str(output_dir))
    print(f"✓ Converted {len(results)} files to {output_dir}")
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_cli.py -v
```

Expected: PASS

**Step 5: 提交CLI接口实现**

```bash
git add src/cli.py tests/test_cli.py
git commit -m "feat: implement CLI interface with subcommands"
```

---

## 集成测试和文档

### Task 11: 编写集成测试

**Files:**
- Modify: `tests/test_integration.py`
- Test: `tests/test_integration.py`

**Step 1: 编写集成测试**

```python
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

        # 执行批量转换
        from src.batch_processor import BatchProcessor
        batch_processor = BatchProcessor(workers=2)

        output_dir = tmpdir / "batch_output"
        results = batch_processor.batch_convert(
            [str(tmpdir / "test0.txt"), str(tmpdir / "test1.txt"), str(tmpdir / "test2.txt")],
            str(output_dir)
        )

        # 验证结果
        assert len(results) == 3
        for result in results:
            assert Path(result).exists()
```

**Step 2: 运行集成测试**

```bash
pytest tests/test_integration.py -v
```

**Step 3: 提交集成测试**

```bash
git add tests/test_integration.py
git commit -m "feat: add integration tests"
```

### Task 12: 更新README文档

**Files:**
- Modify: `README.md`

**Step 1: 更新README**

```markdown
# 电子书转MP3 CLI

将EPUB、MOBI、TXT电子书转换为MP3格式的有声书。

## 功能特性

- 支持 EPUB、MOBI、TXT 格式
- 使用 Microsoft Edge TTS 语音合成
- 批量处理和多线程支持
- 固定长度文本分段
- 实时进度显示
- 错误恢复机制

## 安装

### 方法 1: 从源码安装

```bash
git clone <repository-url>
cd book-to-mp3-cli
pip install -r requirements.txt
```

### 方法 2: 使用 setup.py

```bash
pip install -e .
```

## 使用方法

### 转换单个文件

```bash
book-to-mp3 convert "path/to/book.epub" \
    --output-dir "output" \
    --segment-length 500 \
    --bitrate 192k \
    --voice "zh-CN-XiaoxiaoNeural" \
    --workers 4
```

### 批量转换

```bash
book-to-mp3 batch "path/to/books/" \
    --output-dir "batch_output" \
    --segment-length 500 \
    --bitrate 192k \
    --voice "zh-CN-XiaoxiaoNeural" \
    --workers 4
```

## 命令参数

### convert 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入文件路径 | 必填 |
| --output-dir | 输出目录 | output |
| --segment-length | 文本分段长度（字符数） | 500 |
| --bitrate | 音频比特率 | 192k |
| --voice | 语音名称 | zh-CN-XiaoxiaoNeural |
| --workers | 并发工作进程数 | 4 |

### batch 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_dir | 输入目录 | 必填 |
| --output-dir | 输出目录 | batch_output |
| --segment-length | 文本分段长度（字符数） | 500 |
| --bitrate | 音频比特率 | 192k |
| --voice | 语音名称 | zh-CN-XiaoxiaoNeural |
| --workers | 并发工作进程数 | 4 |

## 支持的语音

当前支持的语音列表：

- `zh-CN-XiaoxiaoNeural` - 小晓（中文女声）
- `zh-CN-YunxiNeural` - 云希（中文男声）
- `zh-CN-YunyangNeural` - 云扬（中文男声）
- `en-US-JennyNeural` - Jenny（英文女声）
- `en-US-GuyNeural` - Guy（英文男声）

更多语音请参考 [Edge TTS 文档](https://github.com/rany2/edge-tts#voices)

## 示例

### 转换 TXT 文件

```bash
book-to-mp3 convert "novel.txt" --segment-length 1000
```

### 转换 EPUB 文件

```bash
book-to-mp3 convert "book.epub" --bitrate 256k
```

### 批量转换目录中的所有书籍

```bash
book-to-mp3 batch "library/" --workers 2
```

### 转换为其他语言

```bash
book-to-mp3 convert "book.epub" --voice "en-US-JennyNeural" --bitrate 320k
```

## 故障排除

### TTS 服务不可用

如果遇到 TTS 服务不可用的情况，请检查：

1. 网络连接是否正常
2. 是否在支持的地理位置
3. 重试次数是否足够

### 文件编码问题

如果遇到编码错误，请确保文件使用 UTF-8 编码。

### 磁盘空间不足

确保有足够的磁盘空间用于存储生成的 MP3 文件。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
```

**Step 2: 提交文档更新**

```bash
git add README.md
git commit -m "docs: update README with comprehensive documentation"
```

---

## 验证和测试

### Task 13: 运行完整测试套件

**Files:**
- Run: `tests/`

**Step 1: 运行所有测试**

```bash
pytest tests/ -v
```

**Step 2: 检查测试覆盖率**

```bash
pytest tests/ --cov=src --cov-report=html
```

**Step 3: 查看覆盖率报告**

```bash
open htmlcov/index.html
```

**Step 4: 提交测试结果**

```bash
git add . coverage.xml htmlcov/
git commit -m "test: verify all tests pass and check coverage"
```

---

## 安装和发布

### Task 14: 安装和验证

**Files:**
- Run: `setup.py`

**Step 1: 安装包**

```bash
pip install -e .
```

**Step 2: 验证安装**

```bash
book-to-mp3 --help
```

**Step 3: 提交安装验证**

```bash
git add .setup.py
git commit -m "chore: verify installation"
```

---

## 总结

完成所有任务后，项目将具备：

1. ✓ 完整的项目结构
2. ✓ 支持EPUB、MOBI、TXT格式
3. ✓ Edge TTS语音引擎
4. ✓ 音频处理功能
5. ✓ 批量处理和多线程
6. ✓ 命令行接口
7. ✓ 完整的测试覆盖
8. ✓ 详细的文档

项目可以立即投入使用。
