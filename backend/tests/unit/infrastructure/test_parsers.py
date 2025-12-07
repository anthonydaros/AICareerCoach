"""Unit tests for document parsers."""

import pytest
import tempfile
import os

from src.infrastructure.parsers import get_parser_for_file
from src.infrastructure.parsers.txt_parser import TxtParser
from src.infrastructure.parsers.pdf_parser import PDFParser
from src.infrastructure.parsers.docx_parser import DocxParser


class TestTxtParser:
    """Test cases for TXT parser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = TxtParser()

    def test_parse_simple_text(self):
        """Test parsing simple text content."""
        content = b"Hello, World!\nThis is a test."
        result = self.parser.parse(content)

        assert "Hello, World!" in result
        assert "This is a test." in result

    def test_parse_utf8_content(self):
        """Test parsing UTF-8 content with special characters."""
        content = "Resume of John Doe\nSkills: Python, JavaScript\nExperience: 5+ years".encode('utf-8')
        result = self.parser.parse(content)

        assert "John Doe" in result
        assert "Python" in result

    def test_parse_empty_content(self):
        """Test parsing empty content."""
        content = b""
        result = self.parser.parse(content)

        assert result == ""

    def test_parse_with_line_breaks(self):
        """Test parsing content with various line breaks."""
        content = b"Line 1\r\nLine 2\nLine 3\rLine 4"
        result = self.parser.parse(content)

        assert "Line 1" in result
        assert "Line 2" in result


class TestParserFactory:
    """Test cases for parser factory."""

    def test_get_parser_for_txt(self):
        """Test getting parser for .txt files."""
        parser = get_parser_for_file("resume.txt")
        assert isinstance(parser, TxtParser)

    def test_get_parser_for_pdf(self):
        """Test getting parser for .pdf files."""
        parser = get_parser_for_file("resume.pdf")
        assert isinstance(parser, PDFParser)

    def test_get_parser_for_docx(self):
        """Test getting parser for .docx files."""
        parser = get_parser_for_file("resume.docx")
        assert isinstance(parser, DocxParser)

    def test_get_parser_for_doc_not_supported(self):
        """Test that .doc files (legacy Word format) raise an error."""
        # python-docx only supports .docx, not legacy .doc format
        with pytest.raises(ValueError, match="No parser available"):
            get_parser_for_file("resume.doc")

    def test_get_parser_for_unknown_extension(self):
        """Test getting parser for unknown file extension."""
        with pytest.raises(ValueError, match="No parser available"):
            get_parser_for_file("resume.xyz")

    def test_get_parser_case_insensitive(self):
        """Test that parser selection is case-insensitive."""
        parser1 = get_parser_for_file("resume.PDF")
        parser2 = get_parser_for_file("resume.TXT")
        parser3 = get_parser_for_file("resume.DOCX")

        assert isinstance(parser1, PDFParser)
        assert isinstance(parser2, TxtParser)
        assert isinstance(parser3, DocxParser)


class TestPDFParser:
    """Test cases for PDF parser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = PDFParser()

    def test_parse_invalid_pdf_raises_error(self):
        """Test that parsing invalid PDF content raises an error."""
        invalid_content = b"This is not a valid PDF"

        with pytest.raises(Exception):
            self.parser.parse(invalid_content)

    def test_parse_empty_content_raises_error(self):
        """Test that parsing empty content raises an error."""
        with pytest.raises(Exception):
            self.parser.parse(b"")


class TestDocxParser:
    """Test cases for DOCX parser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = DocxParser()

    def test_parse_invalid_docx_raises_error(self):
        """Test that parsing invalid DOCX content raises an error."""
        invalid_content = b"This is not a valid DOCX"

        with pytest.raises(Exception):
            self.parser.parse(invalid_content)

    def test_parse_empty_content_raises_error(self):
        """Test that parsing empty content raises an error."""
        with pytest.raises(Exception):
            self.parser.parse(b"")


class TestParserIntegration:
    """Integration tests for parsers with actual files."""

    def test_txt_file_roundtrip(self):
        """Test parsing an actual TXT file."""
        content = "John Doe\nSoftware Engineer\nPython, JavaScript, React"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            parser = get_parser_for_file(temp_path)
            with open(temp_path, 'rb') as f:
                result = parser.parse(f.read())

            assert "John Doe" in result
            assert "Software Engineer" in result
            assert "Python" in result
        finally:
            os.unlink(temp_path)

    def test_parser_supports_method(self):
        """Test that parser supports method works correctly."""
        txt_parser = TxtParser()
        pdf_parser = PDFParser()
        docx_parser = DocxParser()

        assert txt_parser.supports("resume.txt") is True
        assert txt_parser.supports("resume.pdf") is False

        assert pdf_parser.supports("resume.pdf") is True
        assert pdf_parser.supports("resume.txt") is False

        assert docx_parser.supports("resume.docx") is True
        # .doc is legacy format, not supported by python-docx
        assert docx_parser.supports("resume.doc") is False
        assert docx_parser.supports("resume.txt") is False
