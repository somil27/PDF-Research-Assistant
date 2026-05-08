"""Document management routes."""

import logging
from typing import Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.models.schemas import DocumentResponse
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)
router = APIRouter()


def get_document_service() -> DocumentService:
    """Dependency injection for DocumentService."""
    return DocumentService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = "user-default",
    service: DocumentService = Depends(get_document_service),
):
    """Upload and process a PDF document.

    Args:
        file: PDF file to upload
        user_id: User ID (for multi-user support)
        service: Document service

    Returns:
        Document metadata and processing status
    """
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Read file
        content = await file.read()
        if len(content) > 50 * 1024 * 1024:  # 50MB limit
            raise HTTPException(status_code=413, detail="File too large (max 50MB)")

        # Process document
        result = await service.process_pdf(content, file.filename, user_id)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail="Failed to process document")


@router.get("/")
async def list_documents(
    user_id: str = "user-default",
    service: DocumentService = Depends(get_document_service),
):
    """List all documents for a user.

    Args:
        user_id: User ID
        service: Document service

    Returns:
        List of documents
    """
    try:
        documents = await service.get_user_documents(user_id)
        return {"documents": documents, "count": len(documents)}
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to list documents")


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service),
):
    """Get document details.

    Args:
        document_id: Document ID
        service: Document service

    Returns:
        Document details
    """
    try:
        document = await service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(status_code=500, detail="Failed to get document")


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service),
):
    """Delete a document and its chunks.

    Args:
        document_id: Document ID
        service: Document service

    Returns:
        Success message
    """
    try:
        success = await service.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"message": "Document deleted successfully", "id": document_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete document")


@router.get("/{document_id}/status")
async def get_processing_status(
    document_id: str,
    service: DocumentService = Depends(get_document_service),
):
    """Get document processing status.

    Args:
        document_id: Document ID
        service: Document service

    Returns:
        Processing status
    """
    try:
        status = await service.get_processing_status(document_id)
        if status is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get status")
