# Book to MP3 Converter

A Python tool for converting ebooks (EPUB, MOBI, TXT) to MP3 audio files using text-to-speech technology.

## Features

- Convert EPUB, MOBI, and TXT files to audio
- Batch processing support
- Multiple text-to-speech engines
- Configurable output quality
- Command-line interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src.cli convert input.epub output.mp3
```

## Project Structure

```
book-to-mp3/
├── src/
│   ├── parsers/
│   │   ├── epub_parser.py
│   │   ├── mobi_parser.py
│   │   └── txt_parser.py
│   ├── tts_engine.py
│   ├── audio_processor.py
│   ├── batch_processor.py
│   ├── converter.py
│   └── cli.py
├── tests/
│   ├── test_parsers.py
│   ├── test_tts_engine.py
│   ├── test_audio_processor.py
│   ├── test_batch_processor.py
│   └── test_cli.py
├── requirements.txt
├── setup.py
└── README.md
```

## Running Tests

```bash
pytest
```

## License

MIT
