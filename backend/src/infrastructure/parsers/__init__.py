"""Document parsers for various file formats."""

from .pdf_parser import PDFParser
from .docx_parser import DocxParser
from .txt_parser import TxtParser

__all__ = ["PDFParser", "DocxParser", "TxtParser"]


def get_parser_for_file(filename: str):
    """
    Get the appropriate parser for a given file.

    Args:
        filename: Name of the file to parse

    Returns:
        Parser instance that can handle the file

    Raises:
        ValueError: If no parser supports the file type
    """
    parsers = [PDFParser(), DocxParser(), TxtParser()]

    for parser in parsers:
        if parser.supports(filename):
            return parser

    raise ValueError(f"No parser available for file: {filename}")
