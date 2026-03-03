from edge_tts import Communicate
from typing import Optional
from .config import logger

class TtsEngine:
    def __init__(self, voice: str = "zh-CN-XiaoxiaoNeural", rate: str = "+0%"):
        self.voice = voice
        self.rate = rate

    async def text_to_speech(self, text: str, output_path: str, attempts: int = 3) -> Optional[str]:
        for attempt in range(attempts):
            try:
                communicate = Communicate(
                    text,
                    self.voice,
                    rate=self.rate
                )
                await communicate.save(output_path)
                logger.info(f"Generated audio: {output_path}")
                return output_path
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == attempts - 1:
                    raise
