"""PDF document parser using PyMuPDF."""

import fitz  # PyMuPDF


class PDFParser:
    """Parser for PDF documents using PyMuPDF."""

    def parse(self, file_bytes: bytes) -> str:
        """
        Extract text content from PDF bytes.

        Args:
            file_bytes: Raw PDF file bytes

        Returns:
            Extracted text content as string
        """
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            if text.strip():
                text_parts.append(text)

        doc.close()

        return "\n\n".join(text_parts)

    def supports(self, filename: str) -> bool:
        """Check if this parser supports PDF files."""
        return filename.lower().endswith(".pdf")
