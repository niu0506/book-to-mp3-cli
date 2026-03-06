from setuptools import setup, find_packages

setup(
    name="book-to-mp3",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "ebooklib>=0.18",
        "pydub>=0.25.1",
        "edge-tts>=6.1.0",
        "chardet>=5.0.0",
        "tqdm>=4.66.0",
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
    ],
    python_requires=">=3.8",
    author="Book to MP3 Converter",
    description="Convert books to MP3 audio files",
    long_description="Convert EPUB, MOBI, TXT books to MP3 audio files using text-to-speech technology.",
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "book-to-mp3=src.cli:main",
            "book-to-mp3-web=src.web_server:main",
        ],
    },
)
