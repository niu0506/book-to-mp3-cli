from typing import Tuple, Dict
from ..config import logger

class Mobiparser:
    def __init__(self):
        self.supported_formats = ['mobi']
        try:
            from mobi import Mobi
            self.Mobi = Mobi
        except ImportError:
            logger.warning("mobi library not installed. MOBI parsing disabled.")
            self.Mobi = None

    def parse(self, file_path: str) -> Tuple[str, Dict]:
        if self.Mobi is None:
            raise ImportError("mobi library not installed. Install with: pip install mobi")

        mobi = self.Mobi(file_path)
        content = mobi.text

        metadata = {
            'format': 'mobi',
            'language': 'zh-CN',
            'total_length': len(content)
        }

        return content, metadata
