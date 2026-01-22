# Architecture

## Request flow
1. Client calls `POST /chat` with `message` and optional `session_id`.
2. API loads session state (SQLite) and increments turn count.
3. Category is chosen once per session via a keyword classifier (`app/flows/engine.py`).
4. The **required-question gate** enforces intake fields from `configs/flows.yaml`.
5. After required fields are collected, the system queries the KB using TF-IDF retrieval (`app/rag/index.py`).
6. If retrieval confidence is too low (best score < `TIER1_RAG_MIN_SCORE`), the system escalates to a **ticket**.
7. Otherwise it calls the configured LLM provider with:
   - strict Tier0/1 system rules
   - collected intake fields
   - retrieved KB snippets

## Why a state machine layer exists
If you let an LLM “wing it”, you get:
- missing intake fields
- inconsistent troubleshooting
- low quality tickets

The flow config is intentionally outside the model. It’s deterministic and reviewable.

## RAG notes (MVP)
This project uses TF-IDF to avoid external dependencies.

Upgrading to embeddings is a drop-in replacement:
- replace `scripts/ingest_kb.py` and `app/rag/index.py`
- keep the orchestrator logic the same
