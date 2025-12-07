"""Plain text document parser."""


class TxtParser:
    """Parser for plain text documents."""

    def parse(self, file_bytes: bytes) -> str:
        """
        Extract text content from plain text bytes.

        Args:
            file_bytes: Raw text file bytes

        Returns:
            Extracted text content as string
        """
        # Try common encodings
        encodings = ["utf-8", "utf-16", "latin-1", "cp1252"]

        for encoding in encodings:
            try:
                return file_bytes.decode(encoding)
            except (UnicodeDecodeError, LookupError):
                continue

        # Fallback: decode with errors ignored
        return file_bytes.decode("utf-8", errors="ignore")

    def supports(self, filename: str) -> bool:
        """Check if this parser supports text files."""
        return filename.lower().endswith(".txt")
