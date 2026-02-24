from __future__ import annotations

import hashlib
import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path

import yaml

from app.llm.gemini import embed_texts
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


def load_kb_file(fp: Path) -> tuple[DocMeta, list[tuple[str, str]]]:
    if fp.suffix.lower() in (".yaml", ".yml"):
        data = yaml.safe_load(fp.read_text(encoding="utf-8", errors="ignore")) or {}
        category = str(data.get("category") or fp.parent.name)
        title = str(data.get("title") or fp.stem.replace("_", " "))
        doc_id = str(data.get("doc_id") or f"KB-{_stable_id(fp.as_posix())}")
        service = data.get("service")
        tags = list(data.get("tags") or [])
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
    category = str(fm.get("category") or fp.parent.name)
    title = str(fm.get("title") or fp.stem.replace("_", " "))
    doc_id = str(fm.get("doc_id") or f"KB-{_stable_id(fp.as_posix())}")
    service = fm.get("service")
    tags = list(fm.get("tags") or [])
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


async def ingest_kb_dir(kb_dir: Path) -> dict[str, int]:
    files = sorted(list(kb_dir.glob("**/*.md")) + list(kb_dir.glob("**/*.yaml")) + list(kb_dir.glob("**/*.yml")))
    docs = [load_kb_file(fp) for fp in files]

    conn = connect_vec()
    try:
        ensure_vec_schema(conn)
        conn.execute("BEGIN")
        chunk_payloads = _upsert_documents_and_chunks(conn, docs)
        conn.commit()

        texts = [t for _, t in chunk_payloads]
        batch_size = 16
        embeddings: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            embeddings.extend(await embed_texts(texts[i : i + batch_size]))

        cur = conn.cursor()
        for (chunk_id, _), emb in zip(chunk_payloads, embeddings):
            cur.execute(
                "INSERT OR REPLACE INTO kb_vec(chunk_id, embedding) VALUES (?, ?)",
                (chunk_id, struct.pack("%sf" % len(emb), *emb)),
            )
        conn.commit()
    finally:
        conn.close()

    return {
        "files": len(files),
        "docs": len(docs),
        "chunks": len(chunk_payloads),
    }
