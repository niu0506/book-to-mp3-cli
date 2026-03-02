# 电子书转MP3设计文档

## 项目概述

开发一个命令行工具，将EPUB、MOBI、TXT格式的电子书转换为MP3格式的有声书。

## 需求总结

### 核心需求
- **输入格式**：EPUB、MOBI、TXT
- **TTS引擎**：Edge TTS（Microsoft在线语音服务）
- **输出质量**：标准质量（128-192 kbps）
- **使用方式**：命令行（CLI）
- **功能特性**：批量处理、多线程支持
- **分段策略**：固定长度
- **输出位置**：同目录子目录（output子目录）

### 技术约束
- 使用Python 3.8+
- 跨平台支持（Windows/macOS/Linux）
- 异步处理能力

## 系统架构

### 目录结构

```
book-to-mp3-cli/
├── src/
│   ├── __init__.py
│   ├── cli.py              # 命令行接口
│   ├── converter.py        # 核心转换逻辑
│   ├── parsers/            # 格式解析器
│   │   ├── epub_parser.py
│   │   ├── mobi_parser.py
│   │   ├── txt_parser.py
│   │   └── __init__.py
│   ├── tts_engine.py       # TTS引擎封装
│   ├── audio_processor.py  # 音频处理
│   └── batch_processor.py  # 批量处理
├── tests/
│   ├── test_converters.py
│   ├── test_parsers.py
│   ├── test_tts_engine.py
│   └── test_cli.py
├── requirements.txt
├── setup.py
├── README.md
└── LICENSE
```

### 核心模块

#### 1. CLI模块 (`cli.py`)
- 命令行参数解析（使用`argparse`）
- 主函数入口
- 错误处理和用户反馈

#### 2. 格式解析器 (`parsers/`)
- **epub_parser.py**：解析EPUB格式
- **mobi_parser.py**：解析MOBI格式
- **txt_parser.py**：纯文本处理
- 统一接口：返回文本内容和元数据

#### 3. TTS引擎 (`tts_engine.py`)
- 封装`edge-tts`库
- 支持多种语音选择
- 异步处理音频生成
- 重试机制

#### 4. 音频处理 (`audio_processor.py`)
- 使用`pydub`处理音频
- MP3编码（128-192 kbps）
- 音频片段合并
- 编码转换

#### 5. 批量处理器 (`batch_processor.py`)
- 多线程处理（`ProcessPoolExecutor`）
- 进度显示
- 错误隔离（单文件失败不影响其他文件）
- 文件计数器

#### 6. 转换器 (`converter.py`)
- 协调各模块工作
- 流程编排
- 错误处理

## 数据流

```
输入文件 → 格式解析器 → 提取纯文本 → 分段处理 → TTS生成音频 → 
合并音频 → MP3输出
```

## 核心功能设计

### 1. 格式解析

**EPUB解析**：
- 使用`ebooklib`库
- 提取`<body>`内容和元数据
- 保留标题、作者等信息

**MOBI解析**：
- 使用`mobi`或`calibre`命令行工具
- 提取纯文本内容

**TXT解析**：
- 直接读取文件
- 处理编码（UTF-8、GBK等）
- 按行分割

### 2. 分段策略

**固定长度分段**：
- 默认分段：30分钟/段
- 可配置参数：`--segment-length`
- 按字符数而非时间分段（因为TTS生成时间可变）

### 3. TTS生成

**Edge TTS特性**：
- 使用微软Edge浏览器的语音服务
- 支持多种语言和声音
- 高质量语音合成
- 异步API调用

**流程**：
```
文本片段 → 请求Edge TTS → 等待响应 → 保存音频文件
```

### 4. 音频处理

**合并策略**：
- 顺序合并音频片段
- 添加30秒静音间隔
- 保持单声道或立体声

**编码设置**：
```python
encoder_settings = {
    'bitrate': '192k',  # 可选：128k, 192k, 256k, 320k
    'format': 'mp3',
    'quality': 'high'
}
```

### 5. 批量处理

**多线程模型**：
```python
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = []
    for book in books:
        futures.append(executor.submit(process_book, book))
    # 等待所有任务完成
```

**进度显示**：
- 每个文件完成显示进度
- 总体进度条（可选）

**错误恢复**：
- 单个文件失败不影响其他文件
- 记录失败文件到日志
- 可选择继续或停止

## 错误处理

### 分类
1. **文件格式错误**：
   - 提示文件格式不支持
   - 建议转换格式

2. **文件损坏**：
   - 提示文件可能损坏
   - 建议重新下载

3. **TTS错误**：
   - 连接失败：自动重试3次
   - 服务器不可用：提示稍后重试

4. **磁盘空间不足**：
   - 检查可用空间
   - 提示清理磁盘

5. **编码错误**：
   - 尝试多种编码（UTF-8、GBK、GB2312）

### 日志记录
- INFO：正常转换过程
- WARNING：文件跳过、重试
- ERROR：转换失败
- DEBUG：详细调试信息

## 性能考虑

### 优化策略
1. **并发处理**：多线程同时处理多个文件
2. **流式处理**：边生成音频边保存
3. **缓存机制**：缓存已转换的文本片段
4. **资源限制**：限制最大并发数，避免耗尽系统资源

### 性能目标
- 单文件转换：<5分钟（普通长度的书籍）
- 批量处理：基于文件数量和并发数

## 测试策略

### 单元测试
- 测试每个解析器独立功能
- 测试TTS引擎封装
- 测试音频处理逻辑

### 集成测试
- 完整转换流程测试
- 多线程测试
- 错误处理测试

### 边界测试
- 超大文件处理
- 空文件处理
- 罕见编码处理

## 用户交互设计

### 命令行使用

**基本用法**：
```bash
python -m src.cli convert "input.epub"
```

**完整参数**：
```bash
python -m src.cli convert "input.epub" \
    --output-dir "output" \
    --segment-length 30 \
    --bitrate 192k \
    --voice "zh-CN-XiaoxiaoNeural" \
    --workers 4
```

**批量转换**：
```bash
python -m src.cli batch "path/to/books/" \
    --segment-length 30 \
    --workers 4
```

### 输出示例
```
[INFO] Starting conversion of 'book.epub'
[INFO] Extracting text content...
[INFO] Found 45 chapters
[INFO] Converting in parallel with 4 workers...
[PROGRESS] Processing: book.epub (3/10)
[PROGRESS] Processing: book.mobi (5/10)
...
[SUCCESS] Converted 10 files in 45 minutes
```

## 依赖管理

### 核心依赖
- `edge-tts`：TTS引擎
- `ebooklib`：EPUB解析
- `pydub`：音频处理
- `mobi`：MOBI解析
- `chardet`：编码检测

### 可选依赖
- `tqdm`：进度条显示
- `rich`：增强的终端输出

### 版本要求
- Python: >=3.8
- Windows: 支持（依赖edge-tts）
- macOS: 支持
- Linux: 支持（部分语音可能需要额外配置）

## 安全考虑

1. **文件安全**：
   - 验证输入文件路径
   - 防止路径遍历攻击

2. **资源限制**：
   - 限制并发数量
   - 设置超时机制

3. **依赖安全**：
   - 使用官方PyPI仓库
   - 定期更新依赖

## 扩展性

### 未来可能的扩展
1. 支持更多格式（PDF、DOCX）
2. 支持更多TTS引擎（本地引擎、API）
3. GUI界面（基于PyQt或Tkinter）
4. 音频编辑功能（添加背景音乐、配音）
5. 云端批量处理

## 总结

本设计提供了一个完整、可靠的电子书转MP3解决方案，满足用户的所有需求：
- 支持EPUB、MOBI、TXT格式
- 使用Edge TTS高质量语音
- 批量处理和多线程支持
- 固定长度分段
- 同目录子目录输出

项目结构清晰，模块分离，便于维护和扩展。
