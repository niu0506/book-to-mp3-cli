import pytest
from src.text_cleaner import TextCleaner, clean_text


class TestTextCleaner:
    def setup_method(self):
        self.cleaner = TextCleaner()

    def test_clean_basic_text(self):
        text = "这是一个测试文本。"
        result = self.cleaner.clean(text)
        assert result == "这是一个测试文本。"

    def test_remove_control_characters(self):
        text = "Hello\x00World\x07Test"
        result = self.cleaner.clean(text)
        assert "\x00" not in result
        assert "\x07" not in result

    def test_fix_encoding_artifacts(self):
        text = "Test\uFFFDcontent&amp;more"
        result = self.cleaner.clean(text)
        assert "\uFFFD" not in result
        assert "&amp;" not in result
        assert "&" in result

    def test_remove_page_markers(self):
        text = "Page 5\nSome content\n第 10 页\nMore content"
        result = self.cleaner.clean(text)
        assert "Page 5" not in result
        assert "第 10 页" not in result

    def test_normalize_whitespace(self):
        text = "Hello    World\n\n\n\nNew Paragraph"
        result = self.cleaner.clean(text)
        assert "    " not in result

    def test_normalize_punctuation(self):
        text = "Hello,,, World:: test;;;"
        result = self.cleaner.clean(text)
        assert ",,," not in result
        assert "::" not in result

    def test_remove_noise_patterns(self):
        text = "[Illustration] Some text [Image] More text ......"
        result = self.cleaner.clean(text)
        assert "[Illustration]" not in result
        assert "[Image]" not in result

    def test_empty_text(self):
        text = ""
        result = self.cleaner.clean(text)
        assert result == ""

    def test_chinese_page_numbers(self):
        text = "第   1   页\nSome content\n第    10    页\nMore content"
        result = self.cleaner.clean(text)
        assert "第   1   页" not in result
        assert "第    10    页" not in result


class TestCleanTextFunction:
    def test_clean_text_function(self):
        text = "Test  ,,,  text"
        result = clean_text(text)
        assert ",,," not in result
