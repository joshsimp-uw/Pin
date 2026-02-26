#!/usr/bin/env python3
from __future__ import annotations

"""Ingest Knowledge Base files into SQLite + sqlite-vec.

This script is used by scripts/install.sh during `make install`.

It ingests files from the `/knowledge` directory using the currently selected
RAG backend:

- local  -> deterministic offline embeddings, stored in `kb_vec_local`
- gemini -> Gemini embeddings (requires Gemini API key), stored in `kb_vec_gemini`

Backend selection rules (in priority order):
1) Admin-selected backend stored in settings (per org)
2) DEFAULT_RAG_BACKEND env var (local|gemini)
3) Auto: gemini if an org Gemini key exists, otherwise local

Usage:
  python scripts/ingest_kb.py
  python scripts/ingest_kb.py --kb knowledge --org ACME
"""

import argparse
import asyncio
import sys
from pathlib import Path as _Path

# Ensure repo root import works when run from anywhere
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))

from app.core.db import init_schema  # noqa: E402
from app.rag.ingest import ingest_kb_dir  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", default="knowledge", help="Path to knowledge base directory")
    ap.add_argument("--org", default="ACME", help="Organization ID (default: ACME)")
    args = ap.parse_args()

    kb_dir = _Path(args.kb).resolve()
    if not kb_dir.exists() or not kb_dir.is_dir():
        print(f"[ingest_kb] KB dir not found: {kb_dir}")
        return 0  # do not fail install just because KB doesn't exist yet

    # `make install` can run before the bootstrap flow initializes the DB.
    # Ensure schema exists so settings reads and vec tables are available.
    try:
        init_schema()
    except Exception as e:
        print(f"[ingest_kb] Failed to initialize DB schema: {e}")
        return 1

    stats = asyncio.run(ingest_kb_dir(kb_dir, org_id=str(args.org)))
    print(f"[ingest_kb] Done: files={stats.get('files')} docs={stats.get('docs')} chunks={stats.get('chunks')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
