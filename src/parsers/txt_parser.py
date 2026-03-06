import chardet
from typing import Tuple, Dict

class TxtParser:
    def __init__(self):
        self.supported_formats = ['txt']

    def parse(self, file_path: str) -> Tuple[str, Dict]:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        
        encoding = chardet.detect(raw_data)['encoding']
        if not encoding:
            encoding = 'utf-8'
        
        text = raw_data.decode(encoding, errors='replace')
        
        metadata = {
            'format': 'txt',
            'language': 'zh-CN',
            'encoding': encoding,
            'total_length': len(text)
        }
        
        return text, metadata
