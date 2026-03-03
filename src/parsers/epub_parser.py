from ebooklib import epub
from typing import Tuple, Dict

class EpubParser:
    def __init__(self):
        self.supported_formats = ['epub']

    def parse(self, file_path: str) -> Tuple[str, Dict]:
        book = epub.read_epub(file_path)

        content_parts = []
        for item in book.get_items():
            # Get content from all HTML items (this is the current API)
            try:
                content = item.get_content()
                if content:
                    # Decode bytes to string
                    if isinstance(content, bytes):
                        content = content.decode('utf-8', errors='replace')
                    content_parts.append(content)
            except:
                # Skip items that don't have content
                continue

        full_content = ''.join(content_parts)

        metadata = {
            'format': 'epub',
            'language': 'zh-CN',
            'total_length': len(full_content)
        }

        return full_content, metadata
