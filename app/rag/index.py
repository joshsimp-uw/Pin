from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import settings
from app.models.schemas import Citation


@dataclass
class DocChunk:
    source_id: str
    title: str
    text: str
    metadata: dict[str, Any]


@dataclass
class RagIndex:
    vectorizer: TfidfVectorizer
    matrix: Any  # sparse
    chunks: list[DocChunk]


def load_index(path: str | None = None) -> RagIndex:
    p = Path(path or settings.rag_index_path)
    if not p.exists():
        raise FileNotFoundError(
            f"RAG index not found at {p.resolve()}. Run: python scripts/ingest_kb.py"
        )
    with p.open("rb") as f:
        return pickle.load(f)


def retrieve(index: RagIndex, query: str, top_k: int | None = None) -> tuple[list[Citation], float]:
    """Return (citations, best_score)."""
    k = top_k or settings.rag_top_k
    qv = index.vectorizer.transform([query])
    sims = cosine_similarity(qv, index.matrix).ravel()

    if sims.size == 0:
        return [], 0.0

    order = np.argsort(-sims)[:k]
    best = float(sims[order[0]]) if len(order) else 0.0

    citations: list[Citation] = []
    for i in order:
        score = float(sims[i])
        if score <= 0:
            continue
        ch = index.chunks[int(i)]
        snippet = ch.text.strip().replace("\n", " ")
        if len(snippet) > 240:
            snippet = snippet[:240].rstrip() + "..."
        citations.append(
            Citation(
                source_id=ch.source_id,
                title=ch.title,
                snippet=f"[{score:.2f}] {snippet}",
            )
        )
    return citations, best
