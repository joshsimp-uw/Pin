from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration.

    Environment variables are prefixed with TIER1_.

    Examples:
      TIER1_LLM_PROVIDER=mock
      TIER1_OPENAI_API_KEY=...
    """

    model_config = SettingsConfigDict(
        env_prefix="TIER1_",
        env_file=".env",
        extra="ignore",
    )

    # App
    app_name: str = "Tier0/1 Support Assistant"
    environment: str = "dev"

    # Paths
    kb_dir: str = "knowledge"
    # NOTE: legacy TF-IDF index path kept for reference/back-compat, but the
    # current RAG implementation uses SQLite + sqlite-vec.
    rag_index_path: str = "data/rag_index.pkl"
    flow_config_path: str = "configs/flows.yaml"
    sqlite_path: str = "data/pin.db"

    # RAG
    rag_top_k: int = 5
    # For sqlite-vec cosine distance, lower is better; we convert to a
    # similarity-like score via (1 - distance).
    rag_min_score: float = 0.12
    rag_embedding_dim: int = 768

    # LLM provider
    llm_provider: str = "mock"  # mock | openai | gemini
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"  # change as desired
    openai_base_url: str | None = None

    # Gemini
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"
    gemini_embed_model: str = "gemini-embedding-001"
    llm_timeout_s: float = 30.0

    # Admin
    admin_token: str | None = None

    # Guardrails
    max_turns_before_escalate: int = 6
    require_citations: bool = True


settings = Settings()