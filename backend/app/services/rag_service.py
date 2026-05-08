"""Retrieval-Augmented Generation service."""

import logging
import json
from typing import List, Dict, Any, Optional, AsyncGenerator

from openai import AsyncOpenAI

from app.config import get_settings
from app.services.embedding_service import EmbeddingService
from app.models.schemas import SemanticSearchResult, SourceCitation

logger = logging.getLogger(__name__)
settings = get_settings()


class RAGService:
    """Service for Retrieval-Augmented Generation."""

    def __init__(self):
        """Initialize RAG service."""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.embedding_service = EmbeddingService()
        # Mock database for chunks
        self.chunks_db = {}

    async def retrieve_context(
        self,
        query: str,
        document_ids: Optional[List[str]] = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a query.

        Args:
            query: User query
            document_ids: Optional list of document IDs to search
            top_k: Number of results to return

        Returns:
            List of relevant chunks with metadata
        """
        try:
            # Get query embedding
            query_embedding = await self.embedding_service.get_embedding(query)

            # Mock retrieval - in production, use pgvector similarity search
            # This would be: SELECT * FROM chunks WHERE similarity(embedding, query_embedding) > threshold
            # ORDER BY similarity DESC LIMIT top_k

            relevant_chunks = [
                {
                    "id": "chunk-1",
                    "text": "Sample context about the query",
                    "page_number": 1,
                    "filename": "sample.pdf",
                    "similarity_score": 0.95,
                }
            ]

            return relevant_chunks

        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []

    async def stream_response(
        self,
        query: str,
        context: List[Dict[str, Any]],
        conversation_id: str,
    ) -> AsyncGenerator[str, None]:
        """Stream AI response token by token.

        Args:
            query: User query
            context: Retrieved context chunks
            conversation_id: Conversation ID for context

        Yields:
            Response tokens as they arrive
        """
        try:
            # Build context string
            context_str = self._build_context_string(context)

            # Create system message
            system_message = settings.system_prompt

            # Create messages for API
            messages = [
                {"role": "system", "content": system_message},
                {"role": "system", "content": f"Context:\n{context_str}"},
                {"role": "user", "content": query},
            ]

            # Stream response
            async with self.client.messages.stream(
                model=settings.chat_model,
                max_tokens=settings.max_tokens,
                messages=messages,
                temperature=settings.temperature,
            ) as stream:
                async for text in stream.text_stream:
                    # Format as JSON for frontend
                    token_data = json.dumps({
                        "type": "token",
                        "content": text,
                    })
                    yield token_data

                # Send sources at end
                sources = self._extract_sources(context)
                sources_data = json.dumps({
                    "type": "sources",
                    "sources": [s.dict() for s in sources],
                })
                yield sources_data

        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            yield json.dumps({
                "type": "error",
                "content": str(e),
            })

    async def semantic_search(
        self,
        query: str,
        document_ids: Optional[List[str]] = None,
        top_k: int = 5,
    ) -> List[SemanticSearchResult]:
        """Perform semantic search.

        Args:
            query: Search query
            document_ids: Optional list of documents to search
            top_k: Number of results

        Returns:
            List of search results
        """
        try:
            chunks = await self.retrieve_context(query, document_ids, top_k)

            results = [
                SemanticSearchResult(
                    chunk_id=chunk["id"],
                    document_id="doc-id",
                    filename=chunk["filename"],
                    page_number=chunk["page_number"],
                    text=chunk["text"],
                    similarity_score=chunk["similarity_score"],
                )
                for chunk in chunks
            ]

            return results

        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []

    async def find_similar_chunks(
        self,
        chunk_id: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Find chunks similar to a given chunk.

        Args:
            chunk_id: Reference chunk ID
            top_k: Number of results

        Returns:
            List of similar chunks
        """
        # Mock implementation
        return []

    def _build_context_string(self, context: List[Dict[str, Any]]) -> str:
        """Build context string from chunks.

        Args:
            context: List of context chunks

        Returns:
            Formatted context string
        """
        context_parts = []
        for i, chunk in enumerate(context, 1):
            part = f"[{i}] (Page {chunk.get('page_number', '?')} - {chunk.get('filename', 'Unknown')})\n{chunk['text']}"
            context_parts.append(part)
        return "\n\n".join(context_parts)

    def _extract_sources(self, context: List[Dict[str, Any]]) -> List[SourceCitation]:
        """Extract source citations from context.

        Args:
            context: List of context chunks

        Returns:
            List of source citations
        """
        sources = []
        for chunk in context:
            source = SourceCitation(
                document_id=chunk.get("document_id", ""),
                filename=chunk.get("filename", ""),
                page_number=chunk.get("page_number", 0),
                snippet=chunk["text"][:200] + "...",
                similarity_score=chunk.get("similarity_score", 0.0),
            )
            sources.append(source)
        return sources
