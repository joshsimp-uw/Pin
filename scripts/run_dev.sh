#!/usr/bin/env bash
set -euo pipefail
python scripts/ingest_kb.py
exec uvicorn app.main:app --reload --port 8000
