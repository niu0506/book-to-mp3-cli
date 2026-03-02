from pathlib import Path
from typing import Tuple
import asyncio

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
        self.voice = voice
        self.bitrate = bitrate
        self.segment_length = segment_length

    def convert(self, input_file: str, output_dir: str) -> str:
        file_ext = Path(input_file).suffix.lower()
        parser = ParserFactory.get_parser(file_ext)
        text, metadata = parser.parse(input_file)

        audio_processor = AudioProcessor(bitrate=self.bitrate)
        tts_engine = TtsEngine(voice=self.voice)

        segments = audio_processor.split_text_by_length(
            text,
            segment_length=self.segment_length
        )

        audio_files = []
        for i, segment in enumerate(segments):
            output_segment = Path(output_dir) / f"segment_{i}.mp3"
            asyncio.run(tts_engine.text_to_speech(segment, str(output_segment)))
            audio_files.append(str(output_segment))

        output_file = Path(output_dir) / "output.mp3"
        audio_processor.merge_audio(audio_files, str(output_file))

        return str(output_file)
