# Tier0/1 Support Assistant (Capstone MVP)

This is an end-to-end **Tier 0 / Tier 1** company-scoped support assistant.

It includes:
- FastAPI service (`/chat`) with **session state** and a **required-question gate**
- Simple **RAG** pipeline (TF-IDF) over `knowledge/*.md`
- **Escalation to ticket** when documentation is insufficient or turns exceed a limit
- Pluggable LLM layer (`mock` or OpenAI-compatible API)

## 1) Quick start

```bash
cd tier1-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Build the KB index (required once per KB change)
python scripts/ingest_kb.py

# Run the API
uvicorn app.main:app --reload --port 8000
```

Health check:
```bash
curl -s http://localhost:8000/health
```

Create a session:
```bash
curl -s -X POST http://localhost:8000/session/new
```

Chat (example):
```bash
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "session_id": "<paste session id>",
    "message": "VPN fails with error 809",
    "org_id": "acme",
    "user_id": "jsimpson",
    "context": {
      "user_email": "jsimpson@acme.com",
      "device_hostname": "LAPTOP-123"
    }
  }'
```

### How the required-question gate works
The assistant will ask for missing fields one at a time. You can answer naturally, or use key/value lines:

```text
os: Windows 11
device_type: laptop (company-managed)
network_type: home wifi
error_message: 809
mfa_working: yes
```

Once the required fields are collected, it will retrieve KB excerpts and either:
- return an **answer** grounded in sources, or
- return a **ticket** if documentation confidence is low.

## 2) LLM provider configuration

By default, this project uses a deterministic offline provider:

```bash
export TIER1_LLM_PROVIDER=mock
```

To use OpenAI-compatible Chat Completions:

```bash
export TIER1_LLM_PROVIDER=openai
export TIER1_OPENAI_API_KEY='...'
export TIER1_OPENAI_MODEL='gpt-4o-mini'
# Optional if using a proxy or Azure/OpenAI-compatible endpoint
# export TIER1_OPENAI_BASE_URL='https://api.openai.com/v1'
```

## 3) Customize flows (Tier 1 behavior)
Edit `configs/flows.yaml`:
- categories (vpn/email/wifi/etc.)
- required fields per category
- questions per field

This is the “Tier 1 brain”: it forces correct intake before attempting fixes.

## 4) Customize knowledge base (RAG)
Drop markdown files into `knowledge/`.
Then rebuild the index:

```bash
python scripts/ingest_kb.py
```

## 5) Key design rules implemented
- **No doc = escalate**: low retrieval score triggers ticket.
- **Ask first**: required fields are collected before troubleshooting.
- **Company-scoped**: response is instructed to use only KB excerpts.
- **Guardrails**: blocks obviously unsafe guidance and escalates instead.

## 6) Project structure
```
app/
  core/        config + session state (sqlite)
  flows/       required-question engine
  rag/         TF-IDF index + retrieval
  llm/         provider abstraction (mock / OpenAI-compatible)
  policies/    escalation + simple banned-phrase guardrails
  models/      pydantic request/response schemas
knowledge/     your company KB (markdown)
configs/       flow definitions
scripts/       KB ingestion
```

## 7) Next upgrades (if you want to impress the capstone reviewers)
- Swap TF-IDF for embeddings + vector DB (pgvector/Qdrant)
- Add citation enforcement (answer must reference KB sources)
- Add a regression test suite of real tickets (golden set)
- Add auth (OIDC) + org isolation
- Add ITSM integration (ServiceNow/Jira/Zendesk)
