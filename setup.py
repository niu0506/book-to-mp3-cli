from setuptools import setup, find_packages

setup(
    name="book-to-mp3",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "ebooklib>=0.18",
        "requests>=2.31.0",
        "pydub>=0.25.1",
        "speech_recognition>=3.10.0",
        "mutagen>=1.47.0",
        "PyYAML>=6.0.1",
        "edge-tts>=6.1.0",
        "chardet>=5.0.0",
    ],
    python_requires=">=3.7",
    author="Book to MP3 Converter",
    description="Convert books to MP3 audio files",
    long_description=open("README.md").read() if open("README.md").readable() else "",
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "book-to-mp3=src.cli:main",
        ],
    },
)
