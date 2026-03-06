# Book to MP3 Converter

将电子书（EPUB、MOBI、TXT）转换为 MP3 音频文件的工具。

## 功能特性

- 支持多种电子书格式：EPUB、MOBI、TXT
- 使用 Edge-TTS 进行文本转语音
- 提供 CLI 命令行工具和 Web 界面
- 支持批量转换
- 可配置语音、比特率、文本分段长度
- 自动文本清理
- 转换进度显示
- WebSocket 实时通信

## 安装

### 系统要求

- Python >= 3.8
- FFmpeg（用于音频处理）

### 安装依赖

```bash
pip install -r requirements.txt
```

或使用 setup.py 安装：

```bash
pip install -e .
```

### 安装 FFmpeg

**Windows:**
```bash
# 使用 Chocolatey
choco install ffmpeg

# 或从 https://ffmpeg.org/download.html 下载
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

## 使用方法

### Web 界面

启动 Web 服务器：

**Windows:**
```bash
start-web.bat
```

**Linux/macOS:**
```bash
./start-web.sh
```

或直接运行：
```bash
python -m src.web_server
```

访问 http://localhost:5000 使用 Web 界面。

### 命令行工具

#### 转换单个文件

```bash
book-to-mp3 convert <input_file> [选项]
```

选项：
- `--output-dir`: 输出目录（默认：output）
- `--segment-length`: 文本分段长度（默认：500）
- `--bitrate`: 音频比特率（128k/192k/256k/320k，默认：192k）
- `--voice`: 语音名称（默认：zh-CN-XiaoxiaoNeural）
- `--clean-text`: 是否清理文本（默认：True）

示例：
```bash
book-to-mp3 convert book.epub --output-dir audio --bitrate 256k
```

#### 批量转换

```bash
book-to-mp3 batch <input_dir> [选项]
```

选项：
- `--output-dir`: 输出目录（默认：batch_output）
- `--segment-length`: 文本分段长度
- `--bitrate`: 音频比特率
- `--voice`: 语音名称
- `--workers`: 并发工作进程数（默认：4）

示例：
```bash
book-to-mp3 batch ./books --output-dir ./audio --workers 8
```

### 配置文件

创建 `config.yaml` 文件保存默认配置：

```yaml
voice: zh-CN-XiaoxiaoNeural
bitrate: 192k
segment_length: 500
output_dir: output
workers: 4
clean_text: true
```

使用配置文件：
```bash
book-to-mp3 convert book.epub --config config.yaml
```

## 可用语音

常用语音选项：
- `zh-CN-XiaoxiaoNeural` - 中文女声（默认）
- `zh-CN-YunxiNeural` - 中文男声
- `zh-CN-YunyangNeural` - 中文男声（新闻播报风格）
- `en-US-JennyNeural` - 英文女声
- `en-US-GuyNeural` - 英文男声

查看所有可用语音：
```bash
edge-tts --list-voices
```

## 项目结构

```
.
├── data/               # 数据库文件
├── src/
│   ├── parsers/        # 文件解析器（EPUB/MOBI/TXT）
│   ├── web/            # Web 界面
│   │   ├── routers/    # 路由处理
│   │   ├── static/     # 静态文件
│   │   └── templates/  # 模板文件
│   ├── audio_processor.py   # 音频处理
│   ├── batch_processor.py   # 批量处理
│   ├── cli.py               # 命令行接口
│   ├── config.py            # 配置管理
│   ├── converter.py         # 转换核心
│   ├── text_cleaner.py      # 文本清理
│   ├── tts_engine.py        # TTS 引擎
│   └── web_server.py        # Web 服务器
├── uploads/            # 上传文件目录
├── requirements.txt    # 依赖列表
├── setup.py           # 安装配置
└── README.md          # 说明文档
```

## 技术栈

- **Edge-TTS**: 文本转语音
- **Pydub**: 音频处理
- **EbookLib**: EPUB 解析
- **FastAPI**: Web 框架
- **WebSockets**: 实时通信
- **Uvicorn**: ASGI 服务器

## 许可证

MIT License