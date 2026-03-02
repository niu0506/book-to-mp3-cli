from .txt_parser import TxtParser
from .epub_parser import EpubParser
from .mobi_parser import Mobiparser

class ParserFactory:
    _parsers = {
        '.txt': 'TxtParser',
        '.epub': 'EpubParser',
        '.mobi': 'Mobiparser'
    }

    @classmethod
    def get_parser(cls, file_ext: str):
        parser_class_name = cls._parsers.get(file_ext.lower())
        if not parser_class_name:
            raise ValueError(f"Unsupported file format: {file_ext}")

        parser_class = globals()[parser_class_name]
        return parser_class()
