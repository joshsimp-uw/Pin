from __future__ import annotations

import hashlib
import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path

import yaml

from app.core.db import connect
from app.llm.embeddings import embed_texts, get_active_rag_backend
from app.rag.vec_store import connect_vec, ensure_vec_schema


@dataclass
class DocMeta:
    doc_id: str
    title: str
    service: str | None
    category: str
    tags: list[str]
    source_path: str


def _stable_id(*parts: str) -> str:
    h = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()
    return h[:16]


def _split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    _, fm, rest = parts
    try:
        data = yaml.safe_load(fm) or {}
    except Exception:
        data = {}
    return data, rest.lstrip("\n")


def _chunk_markdown_by_h2(md: str) -> list[tuple[str, str]]:
    lines = md.splitlines()
    section_title = "Overview"
    buf: list[str] = []
    out: list[tuple[str, str]] = []

    def flush() -> None:
        nonlocal buf
        body = "\n".join(buf).strip()
        if body:
            out.append((section_title, body))
        buf = []

    for line in lines:
        if line.startswith("## "):
            flush()
            section_title = line[3:].strip() or "Section"
            continue
        if line.startswith("# "):
            continue
        buf.append(line)
    flush()
    return out


def _infer_taxonomy(fp: Path, *, kb_dir: Path) -> tuple[str | None, str | None, str | None]:
    """Infer (device_type, os, application) from:

    knowledge/<device_type>/<operating system>/<application>/<issue.md>
    """
    try:
        rel = fp.resolve().relative_to(kb_dir.resolve())
    except Exception:
        return None, None, None
    parts = list(rel.parts)
    if len(parts) < 4:
        return None, None, None
    device_type, os_name, app_name = parts[0], parts[1], parts[2]
    return device_type, os_name, app_name


def _is_hidden_path(fp: Path, *, kb_dir: Path) -> bool:
    """Return True if any path part under kb_dir starts with '_' or '.'."""
    try:
        rel = fp.resolve().relative_to(kb_dir.resolve())
    except Exception:
        return False
    return any(p.startswith(("_", ".")) for p in rel.parts)


def _kb_file_is_supported(fp: Path, *, kb_dir: Path) -> bool:
    if _is_hidden_path(fp, kb_dir=kb_dir):
        return False
    device_type, os_name, app_name = _infer_taxonomy(fp, kb_dir=kb_dir)
    if not (device_type and os_name and app_name):
        return False
    # Enforce the convention that each issue lives in issue.md
    if fp.suffix.lower() == ".md" and fp.name.lower() != "issue.md":
        return False
    return True


def kb_dir_signature(kb_dir: Path) -> str:
    """Compute a stable signature for KB contents.

    This is used to detect filesystem KB changes and trigger immediate re-ingestion.
    """
    files = sorted(list(kb_dir.glob("**/*.md")) + list(kb_dir.glob("**/*.yaml")) + list(kb_dir.glob("**/*.yml")))
    h = hashlib.sha1()
    for fp in files:
        if not _kb_file_is_supported(fp, kb_dir=kb_dir):
            continue
        try:
            rel = fp.resolve().relative_to(kb_dir.resolve()).as_posix()
        except Exception:
            rel = fp.as_posix()
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(fp.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def _get_kb_state(key: str) -> str | None:
    conn = connect()
    try:
        r = conn.execute("SELECT value_text FROM kb_state WHERE key=?", (key,)).fetchone()
        return str(r["value_text"]) if r else None
    finally:
        conn.close()


def _set_kb_state(key: str, value: str) -> None:
    conn = connect()
    try:
        conn.execute(
            """
            INSERT INTO kb_state(key, value_text, updated_at)
            VALUES(?, ?, datetime('now'))
            ON CONFLICT(key) DO UPDATE SET
              value_text=excluded.value_text,
              updated_at=datetime('now')
            """,
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()


async def rebuild_vectors_from_db(*, backend: str, org_id: str = "ACME") -> dict[str, int | str]:
    """Rebuild the selected vector index from existing kb_chunks.

    Use this when the active RAG backend changes (e.g., local -> gemini) but the
    KB text itself did not.
    """
    from app.llm.providers import LLMError

    conn = connect_vec()
    try:
        ensure_vec_schema(conn, backend=backend)

        rows = conn.execute(
            """
            SELECT c.chunk_id, d.title AS doc_title, c.section_title, c.text
            FROM kb_chunks AS c
            JOIN kb_documents AS d ON d.doc_id = c.doc_id
            ORDER BY c.chunk_id
            """
        ).fetchall()

        # If there are no chunks, nothing to rebuild.
        if not rows:
            return {"chunks": 0, "vectors": 0, "backend_used": backend}

        # Start by clearing the target table for the selected backend.
        table = "kb_vec_gemini" if backend == "gemini" else "kb_vec_local"
        conn.execute(f"DELETE FROM {table}")
        conn.commit()

        texts = [f"{r['doc_title']} — {r['section_title']}\n\n{r['text']}" for r in rows]
        chunk_ids = [str(r["chunk_id"]) for r in rows]

        batch_size = 16
        embeddings: list[list[float]] = []

        try:
            for i in range(0, len(texts), batch_size):
                embeddings.extend(await embed_texts(texts[i : i + batch_size], org_id=org_id, backend=backend))
        except LLMError:
            # If Gemini embeddings fail (missing/invalid key, quota, etc.),
            # fall back to local so startup isn't held hostage.
            if backend == "gemini":
                backend = "local"
                ensure_vec_schema(conn, backend=backend)
                table = "kb_vec_local"
                conn.execute(f"DELETE FROM {table}")
                conn.commit()

                embeddings = []
                for i in range(0, len(texts), batch_size):
                    embeddings.extend(await embed_texts(texts[i : i + batch_size], org_id=org_id, backend=backend))
            else:
                raise

        # Recompute table in case backend changed during fallback.
        table = "kb_vec_gemini" if backend == "gemini" else "kb_vec_local"

        cur = conn.cursor()
        for cid, emb in zip(chunk_ids, embeddings):
            cur.execute(
                f"INSERT OR REPLACE INTO {table}(chunk_id, embedding) VALUES (?, ?)",
                (cid, struct.pack("%sf" % len(emb), *emb)),
            )
        conn.commit()

        return {"chunks": len(rows), "vectors": len(rows), "backend_used": backend}
    finally:
        conn.close()


def load_kb_file(fp: Path, *, kb_dir: Path) -> tuple[DocMeta, list[tuple[str, str]]]:
    if fp.suffix.lower() in (".yaml", ".yml"):
        data = yaml.safe_load(fp.read_text(encoding="utf-8", errors="ignore")) or {}
        device_type, os_name, app_name = _infer_taxonomy(fp, kb_dir=kb_dir)
        category = str(data.get("category") or (f"{device_type}/{os_name}/{app_name}" if device_type else fp.parent.name))
        title = str(data.get("title") or fp.stem.replace("_", " "))
        doc_id = str(data.get("doc_id") or f"KB-{_stable_id(fp.as_posix())}")
        service = data.get("service") or app_name
        tags = list(data.get("tags") or [])
        for extra in [device_type, os_name, app_name]:
            if extra and extra not in tags:
                tags.append(extra)
        meta = DocMeta(
            doc_id=doc_id,
            title=title,
            service=str(service) if service else None,
            category=category,
            tags=[str(t) for t in tags],
            source_path=fp.as_posix(),
        )

        sections: list[tuple[str, str]] = []
        for s in data.get("sections") or []:
            heading = str(s.get("heading") or "Section")
            body = str(s.get("body") or "").strip()
            if body:
                sections.append((heading, body))
        if not sections:
            body = str(data.get("body") or "").strip()
            if body:
                sections = [("Overview", body)]
        return meta, sections

    raw = fp.read_text(encoding="utf-8", errors="ignore")
    fm, body = _split_front_matter(raw)
    device_type, os_name, app_name = _infer_taxonomy(fp, kb_dir=kb_dir)
    category = str(fm.get("category") or (f"{device_type}/{os_name}/{app_name}" if device_type else fp.parent.name))
    title = str(fm.get("title") or fp.stem.replace("_", " "))
    doc_id = str(fm.get("doc_id") or f"KB-{_stable_id(fp.as_posix())}")
    service = fm.get("service") or app_name
    tags = list(fm.get("tags") or [])
    for extra in [device_type, os_name, app_name]:
        if extra and extra not in tags:
            tags.append(extra)
    meta = DocMeta(
        doc_id=doc_id,
        title=title,
        service=str(service) if service else None,
        category=category,
        tags=[str(t) for t in tags],
        source_path=fp.as_posix(),
    )
    return meta, _chunk_markdown_by_h2(body)


def _upsert_documents_and_chunks(conn, docs: list[tuple[DocMeta, list[tuple[str, str]]]]) -> list[tuple[str, str]]:
    chunk_payloads: list[tuple[str, str]] = []
    for meta, sections in docs:
        conn.execute(
            """
            INSERT INTO kb_documents(doc_id, category, title, service, tags_json, source_path)
            VALUES(?,?,?,?,?,?)
            ON CONFLICT(doc_id) DO UPDATE SET
              category=excluded.category,
              title=excluded.title,
              service=excluded.service,
              tags_json=excluded.tags_json,
              source_path=excluded.source_path,
              updated_at=datetime('now')
            """,
            (meta.doc_id, meta.category, meta.title, meta.service, json.dumps(meta.tags), meta.source_path),
        )

        for section_title, text in sections:
            chunk_id = f"{meta.doc_id}:{_stable_id(meta.doc_id, section_title, meta.source_path)}"
            clean = text.strip()
            conn.execute(
                """
                INSERT INTO kb_chunks(chunk_id, doc_id, section_title, heading_path, text)
                VALUES(?,?,?,?,?)
                ON CONFLICT(chunk_id) DO UPDATE SET
                  doc_id=excluded.doc_id,
                  section_title=excluded.section_title,
                  heading_path=excluded.heading_path,
                  text=excluded.text,
                  updated_at=datetime('now')
                """,
                (chunk_id, meta.doc_id, section_title, section_title, clean),
            )
            chunk_payloads.append((chunk_id, f"{meta.title} — {section_title}\n\n{clean}"))
    return chunk_payloads


async def ingest_kb_dir(kb_dir: Path, *, org_id: str = "ACME") -> dict[str, int]:
    files_all = sorted(list(kb_dir.glob("**/*.md")) + list(kb_dir.glob("**/*.yaml")) + list(kb_dir.glob("**/*.yml")))
    files = [fp for fp in files_all if _kb_file_is_supported(fp, kb_dir=kb_dir)]
    docs = [load_kb_file(fp, kb_dir=kb_dir) for fp in files]

    backend = get_active_rag_backend(org_id)

    conn = connect_vec()
    try:
        ensure_vec_schema(conn, backend=backend)
        conn.execute("BEGIN")
        chunk_payloads = _upsert_documents_and_chunks(conn, docs)
        conn.commit()

        texts = [t for _, t in chunk_payloads]
        batch_size = 16

        async def _compute_embeddings(selected_backend: str) -> list[list[float]]:
            embs: list[list[float]] = []
            for i in range(0, len(texts), batch_size):
                embs.extend(await embed_texts(texts[i : i + batch_size], org_id=org_id, backend=selected_backend))
            return embs

        # NOTE: "make install" often runs before any provider keys are configured.
        # If the active backend is "gemini" but the key is missing/invalid, fall
        # back to local embeddings so installation and KB ingestion still succeed.
        try:
            embeddings = await _compute_embeddings(backend)
        except Exception as e:
            from app.llm.providers import LLMError

            if backend == "gemini" and isinstance(e, LLMError):
                backend = "local"
                ensure_vec_schema(conn, backend=backend)
                embeddings = await _compute_embeddings(backend)
            else:
                raise

        cur = conn.cursor()
        table = "kb_vec_gemini" if backend == "gemini" else "kb_vec_local"

        # IMPORTANT:
        # sqlite-vec virtual tables (vec0) can throw UNIQUE constraint errors on
        # repeated ingestion runs even when using INSERT OR REPLACE.
        # To make `make install` idempotent, clear the selected vector table
        # before inserting the newly computed embeddings.
        cur.execute(f"DELETE FROM {table}")

        for (chunk_id, _), emb in zip(chunk_payloads, embeddings):
            cur.execute(
                f"INSERT OR REPLACE INTO {table}(chunk_id, embedding) VALUES (?, ?)",
                (chunk_id, struct.pack("%sf" % len(emb), *emb)),
            )
        conn.commit()
    finally:
        conn.close()

    # Persist signature + backend used so we can auto-sync on startup.
    try:
        _set_kb_state("kb_signature", kb_dir_signature(kb_dir))
        _set_kb_state("kb_last_backend", str(backend))
    except Exception:
        # Don't fail ingestion if state persistence fails.
        pass

    return {
        "files": len(files),
        "docs": len(docs),
        "chunks": len(chunk_payloads),
    }


async def ensure_kb_fresh(kb_dir: Path, *, org_id: str = "ACME") -> dict[str, int]:
    """Ensure the KB + active vector index are up to date.

    Rules:
    - If KB files changed on disk, re-ingest (docs/chunks + vectors).
    - If active RAG backend changed, rebuild vectors for the active backend.
    """
    kb_dir = Path(kb_dir)
    backend = get_active_rag_backend(org_id)

    current_sig = kb_dir_signature(kb_dir) if kb_dir.exists() else ""
    stored_sig = _get_kb_state("kb_signature") or ""
    stored_backend = (_get_kb_state("kb_last_backend") or "").strip().lower()

    # If we have no docs yet, treat as needing ingest.
    conn = connect()
    try:
        r = conn.execute("SELECT COUNT(*) AS n FROM kb_documents").fetchone()
        doc_count = int(r["n"]) if r else 0
    finally:
        conn.close()

    if doc_count == 0 or current_sig != stored_sig:
        return await ingest_kb_dir(kb_dir, org_id=org_id)

    if stored_backend != backend:
        stats = await rebuild_vectors_from_db(backend=backend, org_id=org_id)
        used_backend = str(stats.get("backend_used") or backend)
        try:
            _set_kb_state("kb_last_backend", used_backend)
        except Exception:
            pass
        # Merge stats into the same return shape used elsewhere.
        return {"files": 0, "docs": doc_count, **{k: int(v) if isinstance(v, bool) else v for k, v in stats.items() if k != "backend_used"}, "backend_used": used_backend}

    return {"files": 0, "docs": doc_count, "chunks": 0}