"""Document processing and management service."""

import logging
import io
from typing import Optional, List, Dict, Any
from uuid import uuid4

from app.utils.pdf_parser import PDFParser
from app.utils.text_chunker import TextChunker
from app.services.embedding_service import EmbeddingService
from app.models.schemas import DocumentResponse

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document processing and management."""

    def __init__(self):
        """Initialize document service."""
        self.pdf_parser = PDFParser()
        self.text_chunker = TextChunker()
        self.embedding_service = EmbeddingService()
        # In production, use actual database
        self.documents_db: Dict[str, Any] = {}
        self.chunks_db: Dict[str, List[Any]] = {}

    async def process_pdf(self, content: bytes, filename: str, user_id: str) -> Dict[str, Any]:
        """Process uploaded PDF file.

        Args:
            content: PDF file content
            filename: Original filename
            user_id: User ID

        Returns:
            Document metadata and processing status
        """
        try:
            # Parse PDF
            logger.info(f"Parsing PDF: {filename}")
            file_obj = io.BytesIO(content)
            text, metadata = self.pdf_parser.extract_text(file_obj)

            if not text:
                raise ValueError("No text extracted from PDF")

            # Create document record
            document_id = str(uuid4())
            document_data = {
                "id": document_id,
                "user_id": user_id,
                "filename": filename,
                "file_size": len(content),
                "pages": metadata.get("num_pages", 0),
                "status": "processing",
            }
            self.documents_db[document_id] = document_data

            # Chunk text
            logger.info(f"Chunking text from: {filename}")
            chunks = self.text_chunker.chunk_text(text)

            # Generate embeddings and store chunks
            logger.info(f"Generating embeddings for {len(chunks)} chunks")
            stored_chunks = []
            for idx, chunk in enumerate(chunks):
                # Get embedding
                embedding = await self.embedding_service.get_embedding(chunk["text"])

                chunk_data = {
                    "id": str(uuid4()),
                    "document_id": document_id,
                    "chunk_index": idx,
                    "text": chunk["text"],
                    "page_number": chunk.get("page_number", 1),
                    "embedding": embedding,
                }
                stored_chunks.append(chunk_data)

            self.chunks_db[document_id] = stored_chunks

            # Update document status
            document_data["status"] = "completed"

            logger.info(f"Successfully processed: {filename}")
            return {
                "id": document_id,
                "filename": filename,
                "pages": metadata.get("num_pages", 0),
                "chunks": len(chunks),
                "status": "completed",
            }

        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise

    async def get_user_documents(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all documents for a user.

        Args:
            user_id: User ID

        Returns:
            List of documents
        """
        documents = [
            doc for doc in self.documents_db.values()
            if doc["user_id"] == user_id
        ]
        return documents

    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID.

        Args:
            document_id: Document ID

        Returns:
            Document data or None
        """
        return self.documents_db.get(document_id)

    async def delete_document(self, document_id: str) -> bool:
        """Delete document and associated chunks.

        Args:
            document_id: Document ID

        Returns:
            Success status
        """
        if document_id in self.documents_db:
            del self.documents_db[document_id]
            if document_id in self.chunks_db:
                del self.chunks_db[document_id]
            return True
        return False

    async def get_processing_status(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get document processing status.

        Args:
            document_id: Document ID

        Returns:
            Status information or None
        """
        if document_id not in self.documents_db:
            return None

        doc = self.documents_db[document_id]
        return {
            "id": document_id,
            "status": doc["status"],
            "filename": doc["filename"],
            "chunks": len(self.chunks_db.get(document_id, [])),
        }
