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
    rag_index_path: str = "data/rag_index.pkl"
    flow_config_path: str = "configs/flows.yaml"
    sqlite_path: str = "data/pin.db"

    # RAG
    rag_top_k: int = 5
    rag_min_score: float = 0.12  # cosine similarity threshold for TF-IDF

    # LLM provider
    llm_provider: str = "mock"  # mock | openai
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"  # change as desired
    openai_base_url: str | None = None
    llm_timeout_s: float = 30.0

    # Guardrails
    max_turns_before_escalate: int = 6
    require_citations: bool = True


settings = Settings()