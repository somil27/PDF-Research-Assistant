"""Main API routes."""

from fastapi import APIRouter

from app.api import chat, documents, search

router = APIRouter(prefix="/api", tags=["api"])

# Include route modules
router.include_router(documents.router, prefix="/documents", tags=["documents"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])
router.include_router(search.router, prefix="/search", tags=["search"])
