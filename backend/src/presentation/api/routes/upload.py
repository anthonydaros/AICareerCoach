"""Upload route - File upload and text extraction."""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException

from src.config import get_settings
from src.infrastructure.parsers import get_parser_for_file
from src.presentation.schemas.responses import UploadResponse

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Upload"])

# Magic bytes for file type validation (security measure to prevent file extension spoofing)
MAGIC_BYTES = {
    ".pdf": [b"%PDF"],  # PDF files start with %PDF
    ".docx": [b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"],  # DOCX is a ZIP archive
    ".txt": None,  # No magic bytes for plain text
}


def validate_magic_bytes(content: bytes, extension: str) -> bool:
    """
    Validate file content against expected magic bytes for the extension.

    Args:
        content: File content as bytes
        extension: File extension (e.g., ".pdf")

    Returns:
        True if magic bytes match or no validation needed, False otherwise
    """
    magic_bytes_list = MAGIC_BYTES.get(extension)

    # No magic bytes defined for this extension (e.g., .txt)
    if magic_bytes_list is None:
        return True

    # Check if file starts with any of the expected magic bytes
    for magic in magic_bytes_list:
        if content.startswith(magic):
            return True

    return False


@router.post("/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume file and extract text content.

    Supports PDF, DOCX, and TXT files.

    Args:
        file: Uploaded file (PDF, DOCX, or TXT)

    Returns:
        Extracted text content and metadata
    """
    settings = get_settings()

    # Validate file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    allowed_extensions = settings.get_allowed_extensions_list()
    file_ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(allowed_extensions)}"
        )

    # Read file content
    try:
        content = await file.read()
    except Exception as e:
        logger.error(f"Failed to read file: {e}")
        raise HTTPException(status_code=400, detail="Failed to read file")

    # Check file size
    max_size = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.max_upload_size_mb}MB"
        )

    # SECURITY: Validate magic bytes to prevent file extension spoofing
    if not validate_magic_bytes(content, file_ext):
        logger.warning(f"File upload rejected: magic bytes mismatch for {file.filename}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. The file content does not match the {file_ext} format."
        )

    # Get parser and extract text
    try:
        parser = get_parser_for_file(file.filename)
        text_content = parser.parse(content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to parse file: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract text from file")

    if not text_content.strip():
        raise HTTPException(status_code=400, detail="No text content found in file")

    return UploadResponse(
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        text_content=text_content,
        char_count=len(text_content),
    )
