from typing import List
from pydub import AudioSegment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self, bitrate: str = '192k'):
        self.bitrate = bitrate
        self.silence_duration = 3000

    def split_text_by_length(self, text: str, segment_length: int = 500) -> List[str]:
        return [text[i:min(i + segment_length, len(text))] for i in range(0, len(text), segment_length)]

    def merge_audio(self, audio_files: List[str], output_path: str) -> str:
        if not audio_files:
            raise ValueError("No audio files to merge")

        merged = AudioSegment.empty()

        for audio_file in audio_files:
            audio = AudioSegment.from_mp3(audio_file)
            merged += audio
            merged += AudioSegment.silent(duration=self.silence_duration)

        merged.export(output_path, format="mp3", bitrate=self.bitrate)
        logger.info(f"Merged audio to: {output_path}")
        return output_path
