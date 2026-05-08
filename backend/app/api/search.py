"""Semantic search routes."""

import logging

from fastapi import APIRouter, HTTPException, Depends

from app.models.schemas import SemanticSearchRequest, SemanticSearchResponse
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)
router = APIRouter()


def get_rag_service() -> RAGService:
    """Dependency injection for RAGService."""
    return RAGService()


@router.post("/semantic")
async def semantic_search(
    request: SemanticSearchRequest,
    rag_service: RAGService = Depends(get_rag_service),
):
    """Perform semantic search across documents.

    Args:
        request: Search request with query and optional filters
        rag_service: RAG service

    Returns:
        List of relevant chunks ranked by similarity
    """
    try:
        results = await rag_service.semantic_search(
            query=request.query,
            document_ids=request.document_ids,
            top_k=request.top_k,
        )

        return SemanticSearchResponse(
            query=request.query,
            results=results,
            count=len(results),
        )

    except Exception as e:
        logger.error(f"Error in semantic search: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/similar")
async def find_similar_chunks(
    chunk_id: str,
    top_k: int = 5,
    rag_service: RAGService = Depends(get_rag_service),
):
    """Find chunks similar to a given chunk.

    Args:
        chunk_id: Reference chunk ID
        top_k: Number of results to return
        rag_service: RAG service

    Returns:
        List of similar chunks
    """
    try:
        results = await rag_service.find_similar_chunks(chunk_id, top_k)
        return {"reference_chunk_id": chunk_id, "similar_chunks": results}
    except Exception as e:
        logger.error(f"Error finding similar chunks: {e}")
        raise HTTPException(status_code=500, detail="Failed to find similar chunks")
