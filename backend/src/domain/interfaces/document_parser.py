"""Document parser interface - Port for document parsing."""

from typing import Protocol


class IDocumentParser(Protocol):
    """Protocol for document parser implementations."""

    def parse(self, file_bytes: bytes) -> str:
        """
        Extract text content from document bytes.

        Args:
            file_bytes: Raw file bytes

        Returns:
            Extracted text content as string
        """
        ...

    def supports(self, filename: str) -> bool:
        """
        Check if this parser supports the given file type.

        Args:
            filename: Name of the file to check

        Returns:
            True if this parser can handle the file type
        """
        ...
