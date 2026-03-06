from typing import List
from pathlib import Path
from pydub import AudioSegment
from .config import logger
from .config_handler import DEFAULT_BITRATE, DEFAULT_SEGMENT_LENGTH

class AudioProcessor:
    def __init__(self, bitrate: str = DEFAULT_BITRATE):
        self.bitrate = bitrate
        self.silence_duration = 3000

    def split_text_by_length(self, text: str, segment_length: int = DEFAULT_SEGMENT_LENGTH) -> List[str]:
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
        
        for audio_file in audio_files:
            try:
                Path(audio_file).unlink()
            except Exception as e:
                logger.warning(f"Failed to delete segment file {audio_file}: {e}")
        
        return output_path