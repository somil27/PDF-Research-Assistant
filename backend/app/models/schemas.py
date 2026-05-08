"""Pydantic schemas for API requests/responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Document Schemas
class DocumentMetadata(BaseModel):
    """Document metadata."""

    filename: str
    pages: int
    file_size: int


class DocumentCreate(BaseModel):
    """Create document request."""

    filename: str
    file_size: int


class DocumentResponse(BaseModel):
    """Document response."""

    id: str
    user_id: str
    filename: str
    pages: int
    file_size: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Chunk Schemas
class ChunkResponse(BaseModel):
    """Document chunk response."""

    id: str
    document_id: str
    chunk_index: int
    text: str
    page_number: int
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True


# Chat Schemas
class SourceCitation(BaseModel):
    """Source citation for AI response."""

    document_id: str
    filename: str
    page_number: int
    snippet: str
    similarity_score: float


class Message(BaseModel):
    """Chat message."""

    role: str = Field(..., pattern="^(user|assistant)$")
    content: str
    sources: Optional[list[SourceCitation]] = None
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request."""

    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[str] = None
    document_ids: Optional[list[str]] = None


class ChatResponse(BaseModel):
    """Chat response."""

    conversation_id: str
    message_id: str
    response: str
    sources: list[SourceCitation]
    usage: dict


class ConversationResponse(BaseModel):
    """Conversation response."""

    id: str
    user_id: str
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Search Schemas
class SemanticSearchRequest(BaseModel):
    """Semantic search request."""

    query: str = Field(..., min_length=1, max_length=1000)
    document_ids: Optional[list[str]] = None
    top_k: int = Field(default=5, ge=1, le=20)


class SemanticSearchResult(BaseModel):
    """Semantic search result."""

    chunk_id: str
    document_id: str
    filename: str
    page_number: int
    text: str
    similarity_score: float


class SemanticSearchResponse(BaseModel):
    """Semantic search response."""

    query: str
    results: list[SemanticSearchResult]
    count: int


# Error Schemas
class ErrorResponse(BaseModel):
    """Error response."""

    detail: str
    error_code: str
    timestamp: datetime
