from __future__ import annotations

"""RAG retrieval backed by SQLite + sqlite-vec."""

from app.llm.gemini import embed_texts
from app.rag.vec_store import retrieve_with_scores


async def retrieve(query: str, *, top_k: int | None = None) -> tuple[list, float]:
    """Return (citations, best_score).

    - Embeds the query using Gemini embeddings.
    - Performs KNN search in sqlite-vec.
    """
    vecs = await embed_texts([query])
    return retrieve_with_scores(vecs[0], top_k=top_k)
