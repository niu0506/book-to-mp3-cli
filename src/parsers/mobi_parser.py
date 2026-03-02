from mobi import Mobi
from typing import Tuple, Dict

class Mobiparser:
    def __init__(self):
        self.supported_formats = ['mobi']

    def parse(self, file_path: str) -> Tuple[str, Dict]:
        mobi = Mobi(file_path)
        content = mobi.text
        
        metadata = {
            'format': 'mobi',
            'language': 'zh-CN',
            'total_length': len(content)
        }
        
        return content, metadata
