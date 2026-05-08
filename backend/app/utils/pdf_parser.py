"""PDF parsing utility."""

import logging
from io import BytesIO
from typing import Tuple, Dict, Any

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

logger = logging.getLogger(__name__)


class PDFParser:
    """Parse and extract text from PDF files."""

    def extract_text(self, file_obj: BytesIO) -> Tuple[str, Dict[str, Any]]:
        """Extract text from PDF.

        Args:
            file_obj: File-like object containing PDF

        Returns:
            Tuple of (text, metadata)
        """
        if PdfReader is None:
            raise ImportError("PyPDF2 is required for PDF parsing")

        try:
            pdf = PdfReader(file_obj)
            num_pages = len(pdf.pages)
            text_content = []
            page_mappings = {}  # Track which page each text came from

            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    text_content.append(text)
                    # Store original page number for later reference
                    for _ in text.split():
                        page_mappings[len(text_content)] = page_num

            full_text = "\n\n".join(text_content)

            metadata = {
                "num_pages": num_pages,
                "title": pdf.metadata.title if pdf.metadata else "Unknown",
                "author": pdf.metadata.author if pdf.metadata else "Unknown",
            }

            logger.info(f"Successfully extracted {num_pages} pages from PDF")
            return full_text, metadata

        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise
