"""Chat and conversation management service."""

import logging
from typing import List, Dict, Any, Optional
from uuid import uuid4
from datetime import datetime

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing conversations and messages."""

    def __init__(self):
        """Initialize chat service."""
        # Mock database
        self.conversations_db: Dict[str, Dict[str, Any]] = {}
        self.messages_db: Dict[str, List[Dict[str, Any]]] = {}

    async def create_conversation(self, user_id: str) -> str:
        """Create a new conversation.

        Args:
            user_id: User ID

        Returns:
            Conversation ID
        """
        conversation_id = str(uuid4())
        self.conversations_db[conversation_id] = {
            "id": conversation_id,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        self.messages_db[conversation_id] = []
        logger.info(f"Created conversation: {conversation_id}")
        return conversation_id

    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        sources: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Add a message to conversation.

        Args:
            conversation_id: Conversation ID
            role: Message role (user/assistant)
            content: Message content
            sources: Optional source citations

        Returns:
            Message ID
        """
        message_id = str(uuid4())
        message = {
            "id": message_id,
            "role": role,
            "content": content,
            "sources": sources or [],
            "timestamp": datetime.utcnow().isoformat(),
        }

        if conversation_id not in self.messages_db:
            self.messages_db[conversation_id] = []

        self.messages_db[conversation_id].append(message)
        logger.info(f"Added message to conversation: {conversation_id}")
        return message_id

    async def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get all messages in a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            List of messages
        """
        return self.messages_db.get(conversation_id, [])

    async def get_user_conversations(
        self,
        user_id: str,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Get all conversations for a user.

        Args:
            user_id: User ID
            limit: Maximum number of conversations

        Returns:
            List of conversations
        """
        conversations = [
            conv for conv in self.conversations_db.values()
            if conv["user_id"] == user_id
        ]
        return sorted(
            conversations,
            key=lambda x: x["updated_at"],
            reverse=True,
        )[:limit]
