from __future__ import annotations

import sqlite3
import struct
from pathlib import Path
from typing import Iterable

from app.core.config import settings
from app.models.schemas import Citation


def _serialize_f32(vector: list[float]) -> bytes:
    """Serialize list[float] to sqlite-vec float32 BLOB format."""
    # sqlite-vec expects little-endian float32 packed bytes.
    return struct.pack("%sf" % len(vector), *vector)


def connect_vec() -> sqlite3.Connection:
    """Open a SQLite connection with sqlite-vec loaded."""
    Path(settings.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.sqlite_path)
    conn.row_factory = sqlite3.Row

    # Enable extension loading for this connection and load sqlite-vec.
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")

    try:
        conn.enable_load_extension(True)
    except Exception:
        # Some environments disable extension loading; surface a clear error later.
        pass

    try:
        import sqlite_vec  # type: ignore

        sqlite_vec.load(conn)
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "sqlite-vec is not available. Install dependency 'sqlite-vec' and ensure your "
            "Python sqlite3 build supports extension loading."
        ) from e
    finally:
        try:
            conn.enable_load_extension(False)
        except Exception:
            pass

    return conn


def ensure_vec_schema(conn: sqlite3.Connection) -> None:
    """Create the kb_vec table with the configured embedding dimension if missing.

    NOTE: The base schema file creates kb_vec with float[768]. This function lets you
    create the correct dimension if you deploy with a different embedding size.
    """
    dim = int(settings.rag_embedding_dim)
    conn.execute(
        f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS kb_vec USING vec0(
          chunk_id TEXT PRIMARY KEY,
          embedding float[{dim}] distance_metric=cosine
        );
        """
    )


def upsert_vectors(rows: Iterable[tuple[str, list[float]]]) -> None:
    """Upsert (chunk_id, embedding) rows into kb_vec."""
    conn = connect_vec()
    try:
        ensure_vec_schema(conn)
        cur = conn.cursor()
        for chunk_id, embedding in rows:
            cur.execute(
                "INSERT OR REPLACE INTO kb_vec(chunk_id, embedding) VALUES (?, ?)",
                (chunk_id, _serialize_f32(embedding)),
            )
        conn.commit()
    finally:
        conn.close()


def knn(chunk_query_embedding: list[float], *, top_k: int | None = None) -> list[sqlite3.Row]:
    """Return rows with (chunk_id, distance) from kb_vec."""
    k = int(top_k or settings.rag_top_k)
    conn = connect_vec()
    try:
        ensure_vec_schema(conn)
        q = _serialize_f32(chunk_query_embedding)
        rows = conn.execute(
            """
            SELECT chunk_id, distance
            FROM kb_vec
            WHERE embedding MATCH ?
              AND k = ?
            ORDER BY distance ASC
            """,
            (q, k),
        ).fetchall()
        return rows
    finally:
        conn.close()


def fetch_citations(chunk_ids: list[str]) -> list[Citation]:
    if not chunk_ids:
        return []

    placeholders = ",".join(["?"] * len(chunk_ids))
    conn = connect_vec()
    try:
        rows = conn.execute(
            f"""
            SELECT
              c.chunk_id,
              d.title AS doc_title,
              d.category,
              d.source_path,
              c.section_title,
              c.text
            FROM kb_chunks AS c
            JOIN kb_documents AS d ON d.doc_id = c.doc_id
            WHERE c.chunk_id IN ({placeholders})
            """,
            tuple(chunk_ids),
        ).fetchall()
    finally:
        conn.close()

    by_id = {r["chunk_id"]: r for r in rows}

    citations: list[Citation] = []
    for cid in chunk_ids:
        r = by_id.get(cid)
        if not r:
            continue
        snippet = str(r["text"]).strip().replace("\n", " ")
        if len(snippet) > 240:
            snippet = snippet[:240].rstrip() + "..."
        citations.append(
            Citation(
                source_id=f"{r['source_path']}#{r['section_title']}",
                title=f"{r['doc_title']} — {r['section_title']}",
                snippet=snippet,
            )
        )
    return citations


def retrieve_with_scores(query_embedding: list[float], *, top_k: int | None = None) -> tuple[list[Citation], float]:
    """RAG retrieve: returns (citations, best_score).

    sqlite-vec returns cosine distance when distance_metric=cosine (0 is identical).
    We convert to a similarity-like score via (1 - distance).
    """
    matches = knn(query_embedding, top_k=top_k)
    if not matches:
        return [], 0.0

    chunk_ids = [m["chunk_id"] for m in matches]
    distances = [float(m["distance"]) for m in matches]
    best_sim = max(0.0, 1.0 - float(distances[0])) if distances else 0.0

    citations = fetch_citations(chunk_ids)
    # Prepend scores into snippet for transparency
    for c, d in zip(citations, distances):
        c.snippet = f"[{1.0 - d:.2f}] {c.snippet}"

    return citations, best_sim
