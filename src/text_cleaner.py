import re
from typing import Optional


class TextCleaner:
    def __init__(self, remove_page_markers: bool = True, normalize_whitespace: bool = True):
        self.remove_page_markers = remove_page_markers
        self.normalize_whitespace = normalize_whitespace

    def clean(self, text: str) -> str:
        if not text:
            return text
        
        text = self._remove_control_characters(text)
        text = self._fix_encoding_artifacts(text)
        
        if self.remove_page_markers:
            text = self._remove_page_markers(text)
        
        if self.normalize_whitespace:
            text = self._normalize_whitespace(text)
        
        text = self._normalize_punctuation(text)
        text = self._remove_noise_patterns(text)
        
        return text.strip()

    def _remove_control_characters(self, text: str) -> str:
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

    def _fix_encoding_artifacts(self, text: str) -> str:
        text = re.sub(r'[\uFFFD\uFEFF\u200B-\u200F\u2028-\u202F]', '', text)
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&quot;', '"', text)
        text = re.sub(r'&#\d+;', '', text)
        return text

    def _remove_page_markers(self, text: str) -> str:
        text = re.sub(r'^\s*Page\s+\d+\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*第\s*\d+\s*页\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*[\-\*=_]{3,}\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
        return text

    def _normalize_whitespace(self, text: str) -> str:
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        return text

    def _normalize_punctuation(self, text: str) -> str:
        text = re.sub(r'[,,]+', ',', text)
        text = re.sub(r'[::]+', ':', text)
        text = re.sub(r'[;;]+', ';', text)
        text = re.sub(r'[{}+]+', '+', text)
        text = re.sub(r'[_=]+', '_', text)
        text = re.sub(r'[{}\[\]]+', '', text)
        return text

    def _remove_noise_patterns(self, text: str) -> str:
        text = re.sub(r'\[Illustration[^\]]*\]', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\[Image[^\]]*\]', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\[图[^\]]*\]', '', text)
        text = re.sub(r'\[空白页\]', '', text)
        text = re.sub(r'\.{5,}', '...', text)
        text = re.sub(r'-{3,}', '', text)
        text = re.sub(r'_{3,}', '', text)
        text = re.sub(r'\s*\*+\s*$', '', text, flags=re.MULTILINE)
        return text


def clean_text(text: str, remove_page_markers: bool = True, normalize_whitespace: bool = True) -> str:
    cleaner = TextCleaner(remove_page_markers, normalize_whitespace)
    return cleaner.clean(text)
