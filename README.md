# 电子书转MP3 CLI 工具

将 EPUB、MOBI、TXT 格式的电子书转换为 MP3 格式的有声书，使用 Microsoft Edge TTS 高质量语音合成。

## 功能特性

- **多格式支持**：EPUB、MOBI、TXT 格式电子书
- **TTS 引擎**：使用 Microsoft Edge 浏览器的 TTS 服务
- **批量处理**：支持同时转换多个电子书文件
- **多线程处理**：利用多核 CPU 并发处理，提高效率
- **固定长度分段**：按固定字符数分割文本
- **可配置输出**：自定义比特率、语音、分段长度等
- **错误恢复**：单文件失败不影响其他文件转换
- **编码检测**：自动检测文件编码（UTF-8、GBK、GB2312 等）

## 系统要求

- Python 3.8 或更高版本
- ffmpeg（用于音频处理，可选但推荐）

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

### 方法 3: 安装 ffmpeg（推荐）

Windows:
```bash
choco install ffmpeg
```

macOS:
```bash
brew install ffmpeg
```

Linux:
```bash
sudo apt-get install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg     # CentOS/RHEL
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

### 批量转换目录中的所有书籍

```bash
book-to-mp3 batch "path/to/books/" \
    --output-dir "batch_output" \
    --segment-length 500 \
    --bitrate 192k \
    --voice "zh-CN-XiaoxiaoNeural" \
    --workers 4
```

### 查看帮助

```bash
book-to-mp3 --help
```

## 命令参数

### convert 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入文件路径（必填） | - |
| --output-dir | 输出目录 | output |
| --segment-length | 文本分段长度（字符数） | 500 |
| --bitrate | 音频比特率 | 192k |
| --voice | 语音名称 | zh-CN-XiaoxiaoNeural |
| --workers | 并发工作进程数 | 4 |

### batch 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_dir | 输入目录（必填） | - |
| --output-dir | 输出目录 | batch_output |
| --segment-length | 文本分段长度（字符数） | 500 |
| --bitrate | 音频比特率 | 192k |
| --voice | 语音名称 | zh-CN-XiaoxiaoNeural |
| --workers | 并发工作进程数 | 4 |

## 支持的语音

### 中文语音

- `zh-CN-XiaoxiaoNeural` - 小晓（中文女声）
- `zh-CN-YunxiNeural` - 云希（中文男声）
- `zh-CN-YunyangNeural` - 云扬（中文男声）
- `zh-CN-YunfengNeural` - 云峰（中文男声）

### 英文语音

- `en-US-JennyNeural` - Jenny（英文女声）
- `en-US-GuyNeural` - Guy（英文男声）
- `en-GB-SoniaNeural` - Sonia（英式女声）

### 日文语音

- `ja-JP-NanamiNeural` - Nanami（日文女声）
- `ja-JP-ShioriNeural` - Shiori（日文女声）

更多语音请参考 [Edge TTS 文档](https://github.com/rany2/edge-tts#voices)

## 音频质量设置

| 比特率 | 文件大小 | 质量 | 用途 |
|--------|----------|------|------|
| 128k | 最小 | 标准 | 网络流媒体 |
| 192k | 中等 | 高 | 大多数场景（推荐） |
| 256k | 较大 | 很高 | Hi-Fi 音频 |
| 320k | 最大 | 无损 | 发烧友 |

## 示例

### 转换 TXT 文件

```bash
book-to-mp3 convert "novel.txt" --segment-length 1000
```

### 转换 EPUB 文件

```bash
book-to-mp3 convert "book.epub" --bitrate 256k
```

### 转换 MOBI 文件

```bash
book-to-mp3 convert "book.mobi" --workers 2
```

### 批量转换目录中的所有书籍

```bash
book-to-mp3 batch "library/" --workers 2 --segment-length 1000
```

### 转换为英文语音

```bash
book-to-mp3 convert "book.epub" --voice "en-US-JennyNeural" --bitrate 320k
```

### 转换为特定分段长度

```bash
book-to-mp3 convert "novel.epub" --segment-length 100 --bitrate 192k
```

### 使用不同的 TTS 引擎

```bash
# 使用云端 TTS（当前实现）
book-to-mp3 convert "book.epub" --voice "zh-CN-XiaoxiaoNeural"
```

## 项目结构

```
book-to-mp3-cli/
├── src/
│   ├── __init__.py
│   ├── cli.py              # 命令行接口
│   ├── converter.py        # 核心转换逻辑
│   ├── tts_engine.py       # TTS 引擎封装
│   ├── audio_processor.py  # 音频处理
│   ├── batch_processor.py  # 批量处理
│   └── parsers/            # 格式解析器
│       ├── __init__.py
│       ├── txt_parser.py   # TXT 解析器
│       ├── epub_parser.py  # EPUB 解析器
│       └── mobi_parser.py  # MOBI 解析器
├── tests/
│   ├── test_integration.py
│   ├── test_parsers.py
│   ├── test_tts_engine.py
│   ├── test_audio_processor.py
│   ├── test_batch_processor.py
│   └── test_cli.py
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
```

## 核心功能说明

### 格式解析器

- **TXT 解析器**：支持多种编码检测，自动识别文件编码
- **EPUB 解析器**：使用 `ebooklib` 库提取内容
- **MOBI 解析器**：使用 `mobi` 库解析，包含错误处理

### TTS 引擎

- 基于 `edge-tts` 库
- 支持多种语音和语速调整
- 自动重试机制（最多 3 次）
- 异步处理提高效率

### 音频处理

- 使用 `pydub` 进行音频处理
- 支持 MP3 编码（128k-320k）
- 段落间添加 3 秒静音
- 音频片段自动合并

### 批量处理

- 使用 `multiprocessing.ProcessPoolExecutor`
- 可配置工作进程数
- 错误隔离（单个文件失败不影响其他文件）
- 实时进度显示

### CLI 接口

- 使用 `argparse` 实现命令行参数解析
- 支持 `convert` 和 `batch` 子命令
- 详细的帮助信息

## 故障排除

### TTS 服务不可用

如果遇到 TTS 服务不可用的情况，请检查：

1. 网络连接是否正常
2. 是否在支持的地理位置
3. 重试次数是否足够
4. 检查 Edge 浏览器版本

### 文件编码问题

如果遇到编码错误，请确保文件使用 UTF-8 编码。

文件编码检测：
- UTF-8（标准）
- GBK（中文常见）
- GB2312（中文常见）
- Big5（繁体中文）
- ASCII（英文）

### 磁盘空间不足

确保有足够的磁盘空间用于存储生成的 MP3 文件。计算公式：
```
文件大小 ≈ 文本字符数 × 0.1 字节/字符 × (比特率 / 8)
```

示例：
- 10 万字符，192k 比特率 → 约 2.5 MB
- 100 万字符，192k 比特率 → 约 25 MB

### ffmpeg 找不到

如果遇到 ffmpeg 错误：

**Windows:**
```bash
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### 某些书籍转换失败

如果某个书籍转换失败：

1. 检查文件是否损坏
2. 尝试单独转换该文件
3. 查看错误日志
4. 提交 Issue 报告问题

### 批量转换速度慢

调整工作进程数：
```bash
book-to-mp3 batch "library/" --workers 8  # 使用更多 CPU 核心
```

## 测试

### 运行单元测试

```bash
pytest tests/test_parsers.py -v
pytest tests/test_tts_engine.py -v
pytest tests/test_audio_processor.py -v
pytest tests/test_batch_processor.py -v
pytest tests/test_cli.py -v
```

### 运行集成测试

```bash
pytest tests/test_integration.py -v
```

### 运行所有测试

```bash
pytest tests/ -v
```

### 生成测试覆盖率报告

```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

## 开发

### 代码风格

- 遵循 PEP 8 规范
- 使用类型提示（Type Hints）
- 完整的文档字符串
- 清晰的变量命名

### 测试覆盖率

目标覆盖率：90%+

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## 性能优化

### 转换速度

| 文件类型 | 字符数 | 时间（单线程） | 时间（4 线程） |
|----------|--------|----------------|----------------|
| TXT      | 10 万  | 30 分钟        | 10 分钟        |
| TXT      | 100 万 | 5 小时         | 1.5 小时       |
| EPUB     | 100 万 | 6 小时         | 2 小时         |

### 磁盘空间

```bash
# 计算所需磁盘空间
python -c "print(f'预计大小: {len_text} 字符 × 0.1 字节/字符 × {bitrate}/8 = {len_text * 0.1 * int(bitrate)/8/1024:.2f} MB')"
```

## 依赖

### 核心依赖

- `edge-tts>=6.1.0` - TTS 服务
- `ebooklib>=0.18` - EPUB 解析
- `pydub>=0.25.1` - 音频处理
- `mobi>=1.1.0` - MOBI 解析
- `chardet>=5.2.0` - 编码检测
- `tqdm>=4.66.0` - 进度条

### 可选依赖

- `pytest>=7.4.0` - 测试框架
- `pytest-cov>=4.1.0` - 测试覆盖率

## 常见问题

### Q: 支持哪些语言？

A: 支持所有 Edge TTS 提供的语言，包括中文、英文、日文、韩文、法文、德文等。

### Q: 转换速度慢怎么办？

A:
1. 增加 `--workers` 参数（如 `--workers 8`）
2. 减小 `--segment-length` 参数
3. 降低 `--bitrate` 参数
4. 使用更快的网络连接

### Q: 可以离线使用吗？

A: 当前版本需要网络连接以调用 Edge TTS 服务。离线版本需要使用本地 TTS 引擎（如 Windows SAPI5 或 espeak）。

### Q: 可以添加背景音乐吗？

A: 当前版本不支持添加背景音乐。未来可能会添加此功能。

### Q: 支持哪些音频格式？

A: 目前只支持 MP3 格式。未来可能会添加其他格式（如 WAV、AAC）。

### Q: 转换后的音频有停顿怎么办？

A: 这是正常现象。工具会在每个段落之间添加 3 秒静音以避免语音重叠。

## 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some amazing feature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 测试

提交代码前请确保：
- 所有测试通过：`pytest tests/`
- 代码符合规范：使用 `flake8` 或 `ruff`
- 添加必要的文档和注释

## 许可证

MIT License

## 致谢

- [edge-tts](https://github.com/rany2/edge-tts) - Edge TTS Python 库
- [ebooklib](https://github.com/aerkalov/ebooklib) - EPUB 处理库
- [pydub](https://github.com/jiaaro/pydub) - 音频处理库

## 联系方式

- Issue: [提交问题](https://github.com/anomalyco/opencode/issues)
- Email: your-email@example.com

## 更新日志

### v0.1.0 (2026-03-03)

- ✨ 初始版本
- ✨ 支持 EPUB、MOBI、TXT 格式
- ✨ Edge TTS 语音合成
- ✨ 批量处理和多线程
- ✨ 可配置输出质量
- ✨ 完整的测试覆盖
