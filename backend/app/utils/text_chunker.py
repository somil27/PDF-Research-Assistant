"""Text chunking utility for RAG."""

import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class TextChunker:
    """Split text into chunks for embedding."""

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
        separator: str = "\n\n",
    ):
        """Initialize text chunker.

        Args:
            chunk_size: Target chunk size in tokens
            overlap: Number of overlapping tokens
            separator: Separator for splitting
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separator = separator

    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Split text into chunks.

        Args:
            text: Text to chunk

        Returns:
            List of chunks with metadata
        """
        try:
            # Clean text
            text = self._clean_text(text)

            # Split by separator first
            sections = text.split(self.separator)

            chunks = []
            current_chunk = ""
            page_number = 1

            for section in sections:
                if not section.strip():
                    continue

                # Check if adding this section would exceed chunk size
                combined = current_chunk + self.separator + section if current_chunk else section
                tokens = self._estimate_tokens(combined)

                if tokens > self.chunk_size and current_chunk:
                    # Save current chunk and start new one
                    chunk_data = {
                        "text": current_chunk.strip(),
                        "page_number": page_number,
                    }
                    chunks.append(chunk_data)

                    # Start new chunk with overlap
                    overlap_text = self._get_overlap_text(current_chunk)
                    current_chunk = overlap_text + self.separator + section
                else:
                    current_chunk = combined

            # Add final chunk
            if current_chunk.strip():
                chunk_data = {
                    "text": current_chunk.strip(),
                    "page_number": page_number,
                }
                chunks.append(chunk_data)

            logger.info(f"Created {len(chunks)} chunks from text")
            return chunks

        except Exception as e:
            logger.error(f"Error chunking text: {e}")
            return []

    def _clean_text(self, text: str) -> str:
        """Clean text for processing.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r"[^\w\s\.\'\,\-\!\?\(\)\[\]]", "", text)
        return text.strip()

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation).

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        # Rough estimation: ~1 token per 4 characters
        return len(text) // 4

    def _get_overlap_text(self, text: str) -> str:
        """Get overlap portion of text.

        Args:
            text: Text to extract overlap from

        Returns:
            Overlap portion
        """
        # Get the last portion that fits in overlap
        overlap_chars = self.overlap * 4  # Rough reverse estimate
        return text[-overlap_chars:] if len(text) > overlap_chars else text
