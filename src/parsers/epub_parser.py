from ebooklib import epub
from typing import Tuple, Dict

class EpubParser:
    def __init__(self):
        self.supported_formats = ['epub']

    def parse(self, file_path: str) -> Tuple[str, Dict]:
        book = epub.read_epub(file_path)
        
        content_parts = []
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                content_parts.append(item.get_content())
        
        full_content = ''.join(content_parts)
        
        metadata = {
            'format': 'epub',
            'language': 'zh-CN',
            'total_length': len(full_content)
        }
        
        return full_content, metadata
