#!/usr/bin/env python3
from __future__ import annotations

"""Convert structured Markdown KB files to YAML KB files.

This is optional, but some teams find YAML easier to parse/validate than
Markdown with headings.

Input:
  knowledge/**/*.md

Output (default):
  knowledge_yaml/.../*.yaml

YAML schema:
  doc_id: KB-...
  title: ...
  category: ...
  service: ...
  tags: [...]
  sections:
    - heading: ...
      body: |-
        ...
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path as _Path

import yaml

sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))

from app.core.config import settings


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


def convert_file(fp: _Path, out_root: _Path) -> _Path:
    raw = fp.read_text(encoding="utf-8", errors="ignore")
    fm, body = _split_front_matter(raw)

    category = str(fm.get("category") or fp.parent.name)
    title = str(fm.get("title") or fp.stem.replace("_", " "))
    doc_id = str(fm.get("doc_id") or f"KB-{_stable_id(fp.as_posix())}")

    data = {
        "doc_id": doc_id,
        "title": title,
        "category": category,
        "service": fm.get("service"),
        "tags": list(fm.get("tags") or []),
        "sections": [
            {"heading": heading, "body": section}
            for heading, section in _chunk_markdown_by_h2(body)
        ],
    }

    rel = fp.relative_to(fp.parents[1])  # knowledge/.../file.md -> .../file.md
    out_path = out_root / rel
    out_path = out_path.with_suffix(".yaml")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert KB markdown files to YAML")
    parser.add_argument("--kb", default=settings.kb_dir, help="KB directory")
    parser.add_argument("--out", default="knowledge_yaml", help="Output directory")
    args = parser.parse_args()

    kb_dir = _Path(args.kb)
    out_root = _Path(args.out)
    if not kb_dir.exists():
        raise SystemExit(f"KB dir not found: {kb_dir.resolve()}")

    files = sorted(kb_dir.glob("**/*.md"))
    if not files:
        raise SystemExit(f"No markdown files found under: {kb_dir.resolve()}")

    for fp in files:
        out = convert_file(fp, out_root)
        print(f"{fp} -> {out}")


if __name__ == "__main__":
    main()
