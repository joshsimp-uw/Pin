from __future__ import annotations

"""RAG retrieval backed by SQLite + sqlite-vec."""

from app.llm.embeddings import embed_texts, get_active_rag_backend
from app.rag.vec_store import retrieve_with_scores


async def retrieve(query: str, *, org_id: str, top_k: int | None = None) -> tuple[list, float]:
    """Return (citations, best_score).

    - Embeds the query using Gemini embeddings.
    - Performs KNN search in sqlite-vec.
    """
    backend = get_active_rag_backend(org_id)
    vecs = await embed_texts([query], org_id=org_id, backend=backend)
    return retrieve_with_scores(vecs[0], top_k=top_k, backend=backend)
