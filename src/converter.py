from pathlib import Path
from typing import Callable, Optional
import asyncio
from tqdm import tqdm

from .parsers import ParserFactory
from .tts_engine import TtsEngine
from .audio_processor import AudioProcessor
from .text_cleaner import TextCleaner
from .config_handler import DEFAULT_VOICE, DEFAULT_BITRATE, DEFAULT_SEGMENT_LENGTH
from .utils import call_progress_callback, safe_file_operation


class Converter:
    def __init__(
        self,
        voice: str = DEFAULT_VOICE,
        bitrate: str = DEFAULT_BITRATE,
        segment_length: int = DEFAULT_SEGMENT_LENGTH,
        clean_text: bool = True,
        progress_callback: Optional[Callable] = None
    ):
        self.voice = voice
        self.bitrate = bitrate
        self.segment_length = segment_length
        self.clean_text = clean_text
        self.text_cleaner = TextCleaner()
        self.progress_callback = progress_callback

    def convert(self, input_file: str, output_dir: str, output_filename: Optional[str] = None) -> str:
        file_ext = Path(input_file).suffix.lower()
        parser = ParserFactory.get_parser(file_ext)
        text, metadata = parser.parse(input_file)

        if self.clean_text:
            text = self.text_cleaner.clean(text)

        safe_file_operation(
            lambda: Path(output_dir).mkdir(parents=True, exist_ok=True),
            output_dir,
            "创建输出目录"
        )

        audio_processor = AudioProcessor(bitrate=self.bitrate)
        tts_engine = TtsEngine(voice=self.voice)

        segments = audio_processor.split_text_by_length(
            text,
            segment_length=self.segment_length
        )

        audio_files = []
        
        async def generate_segment(segment: str, output_segment: Path, index: int) -> str:
            await tts_engine.text_to_speech(segment, str(output_segment))
            return str(output_segment)

        segments_with_paths = [
            (segment, Path(output_dir) / f"segment_{i}.mp3", i)
            for i, segment in enumerate(segments)
        ]

        tasks = [
            generate_segment(segment, path, index)
            for segment, path, index in segments_with_paths
        ]

        with tqdm(total=len(tasks), desc="生成音频", unit="段") as pbar:
            async def generate_with_progress():
                results = []
                for task in asyncio.as_completed(tasks):
                    result = await task
                    results.append(result)
                    pbar.update(1)
                    if self.progress_callback:
                        progress = len(results) / len(tasks) * 100
                        call_progress_callback(
                            callback=self.progress_callback,
                            progress=progress,
                            current_segment=len(results),
                            total_segments=len(tasks),
                            current_text_preview=segments[len(results)-1][:50] if len(results) <= len(segments) else ""
                        )
                return results

            audio_files = asyncio.run(generate_with_progress())

        if output_filename is None:
            output_filename = "output.mp3"
        output_file = Path(output_dir) / output_filename
        audio_processor.merge_audio(audio_files, str(output_file))

        return str(output_file)