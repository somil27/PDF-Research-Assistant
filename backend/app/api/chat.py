"""Chat and RAG routes."""

import logging
from typing import Optional, AsyncGenerator

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)
router = APIRouter()


def get_chat_service() -> ChatService:
    """Dependency injection for ChatService."""
    return ChatService()


def get_rag_service() -> RAGService:
    """Dependency injection for RAGService."""
    return RAGService()


@router.post("/message")
async def send_message(
    request: ChatRequest,
    user_id: str = "user-default",
    chat_service: ChatService = Depends(get_chat_service),
    rag_service: RAGService = Depends(get_rag_service),
):
    """Send a chat message and get AI response with streaming.

    Args:
        request: Chat request with message and optional context
        user_id: User ID
        chat_service: Chat service
        rag_service: RAG service

    Returns:
        Streaming response with token-by-token content
    """
    try:
        async def generate():
            """Generate streaming response."""
            try:
                # Get or create conversation
                if not request.conversation_id:
                    conversation_id = await chat_service.create_conversation(user_id)
                else:
                    conversation_id = request.conversation_id

                # Retrieve relevant chunks
                context_chunks = await rag_service.retrieve_context(
                    query=request.message,
                    document_ids=request.document_ids,
                    top_k=5,
                )

                if not context_chunks:
                    yield "data: {\"error\": \"No relevant documents found\"}"
                    return

                # Stream response
                async for token in rag_service.stream_response(
                    query=request.message,
                    context=context_chunks,
                    conversation_id=conversation_id,
                ):
                    yield f"data: {token}\n\n"

            except Exception as e:
                logger.error(f"Error in message streaming: {e}")
                yield f"data: {{\"error\": \"{str(e)}\"}}"

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail="Failed to send message")


@router.post("/new")
async def create_conversation(
    user_id: str = "user-default",
    chat_service: ChatService = Depends(get_chat_service),
):
    """Create a new conversation.

    Args:
        user_id: User ID
        chat_service: Chat service

    Returns:
        Conversation ID
    """
    try:
        conversation_id = await chat_service.create_conversation(user_id)
        return {"id": conversation_id, "user_id": user_id}
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail="Failed to create conversation")


@router.get("/history/{conversation_id}")
async def get_conversation_history(
    conversation_id: str,
    chat_service: ChatService = Depends(get_chat_service),
):
    """Get conversation history.

    Args:
        conversation_id: Conversation ID
        chat_service: Chat service

    Returns:
        List of messages in conversation
    """
    try:
        history = await chat_service.get_conversation_history(conversation_id)
        return {"id": conversation_id, "messages": history}
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversation history")
