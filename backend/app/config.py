"""Application configuration."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "PDF Research Assistant"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # OpenAI Configuration
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000

    # Supabase Configuration
    supabase_url: str
    supabase_service_role_key: str
    database_url: str

    # RAG Configuration
    max_chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_retrieval: int = 5
    min_similarity_score: float = 0.5

    # Logging
    log_level: str = "INFO"

    # System Prompt
    system_prompt: str = """You are a helpful AI assistant specialized in answering questions about documents.

Guidelines:
1. Answer questions based ONLY on the provided document context
2. Always cite your sources with specific page numbers
3. If information isn't in the documents, clearly state that
4. Provide accurate, well-sourced answers
5. Format your response clearly with proper markdown
6. Include direct quotes when relevant

When citing sources, use this format:
[Source: Filename, Page X]
"""

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
