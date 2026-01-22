#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))


import argparse
import pickle
from dataclasses import asdict
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer

from app.core.config import settings
from app.rag.index import DocChunk, RagIndex


def chunk_text(text: str, max_chars: int = 1600, overlap: int = 200) -> list[str]:
    """Simple char-based chunker.

    For a capstone MVP, this is good enough. If you want to level up later:
      - chunk by headings
      - keep procedure blocks intact
      - add overlap by token count (tiktoken)
    """
    text = "\n".join([line.rstrip() for line in text.splitlines()]).strip()
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
        if end == len(text):
            break
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Build TF-IDF RAG index from knowledge/*.md")
    parser.add_argument("--kb", default=settings.kb_dir, help="KB directory")
    parser.add_argument("--out", default=settings.rag_index_path, help="Output pickle path")
    args = parser.parse_args()

    kb_dir = Path(args.kb)
    if not kb_dir.exists():
        raise SystemExit(f"KB dir not found: {kb_dir.resolve()}")

    files = sorted(kb_dir.glob("**/*.md"))
    if not files:
        raise SystemExit(f"No markdown files found under: {kb_dir.resolve()}")

    chunks: list[DocChunk] = []
    for fp in files:
        title = fp.stem.replace("_", " ")
        text = fp.read_text(encoding="utf-8", errors="ignore")
        for idx, ch in enumerate(chunk_text(text)):
            chunks.append(
                DocChunk(
                    source_id=f"{fp.as_posix()}#{idx}",
                    title=title,
                    text=ch,
                    metadata={"path": fp.as_posix()},
                )
            )

    corpus = [c.text for c in chunks]
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        max_features=150_000,
        ngram_range=(1, 2),
    )
    matrix = vectorizer.fit_transform(corpus)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    index = RagIndex(vectorizer=vectorizer, matrix=matrix, chunks=chunks)
    with out_path.open("wb") as f:
        pickle.dump(index, f)

    print(f"Indexed {len(chunks)} chunks from {len(files)} files")
    print(f"Wrote: {out_path.resolve()}")


if __name__ == "__main__":
    main()
