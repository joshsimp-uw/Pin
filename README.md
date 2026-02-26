# Pin

Pin is an AI-powered IT support assistant that uses Retrieval-Augmented
Generation (RAG) against a structured knowledge base to troubleshoot
supported systems and escalate unsupported requests into tickets.

Designed for controlled enterprise environments where scope enforcement,
determinism, and offline capability matter.

------------------------------------------------------------------------

# Overview

Pin provides:

-   Structured Knowledge Base ingestion
-   Local offline vector database (no external API required)
-   Optional Gemini embeddings via Google AI Studio
-   Admin-switchable RAG backend (Local ↔ Gemini)
-   Enforced support boundaries based on KB structure
-   Automatic escalation for unsupported systems
-   Multi-organization support

------------------------------------------------------------------------

# Architecture

    User
      ↓
    FastAPI (app.main)
      ↓
    Support Scope Validator (device / OS / app check)
      ↓
    RAG Retrieval Layer
          ↙              ↘
     Local Vector DB     Gemini Vector DB
     (sqlite-vec)        (Google AI Studio)
          ↓
    LLM Response
      ↓
    Escalation Logic (if unsupported or no match)

Key components:

-   `app/main.py` --- API entry point
-   `app/rag/` --- ingestion, indexing, retrieval
-   `app/knowledge/` --- support scope enforcement
-   `knowledge/` --- structured KB source
-   SQLite DB --- metadata + vector storage

------------------------------------------------------------------------

# Knowledge Base Structure (Required)

The knowledge base must follow this directory layout:

    knowledge/<device_type>/<operating_system>/<application>/<issue>.md

Example:

    knowledge/
      laptop-notebook/
        windows-11/
          outlook/
            profile-corruption.md

## Supported Devices

Only device types present as directories under `/knowledge` are
supported.

Default expected device types:

-   mobile\
-   tablet\
-   laptop-notebook\
-   desktop\

If a user requests support for:

-   A device type not present
-   An OS not under that device
-   An application not under that OS

The request is automatically escalated as **unsupported**.

To add support:

1.  Create appropriate folder structure
2.  Add markdown KB files
3.  Re-ingest via Admin panel

------------------------------------------------------------------------

# RAG Backends

Pin supports two embedding backends.

## 1. Local (Default / Offline Mode)

-   Uses sqlite-vec
-   Deterministic embeddings
-   No external API calls
-   Fully functional offline

Vector table:

    kb_vec_local

Recommended for:

-   Air-gapped environments
-   No external dependencies
-   Secure internal deployments

------------------------------------------------------------------------

## 2. Gemini (Optional)

If a Gemini API key is configured:

-   Embeddings generated via Google AI Studio
-   Higher dimensional vectors
-   Stored in:

```{=html}
<!-- -->
```
    kb_vec_gemini

If no Gemini key is configured, system defaults to Local backend.

------------------------------------------------------------------------

# Switching RAG Backend

Admin interface:

    Admin → RAG Settings

Available actions:

-   Select backend (`local` or `gemini`)
-   Save configuration
-   Re-ingest knowledge base

API:

    GET  /api/admin/rag
    PUT  /api/admin/rag
    POST /api/admin/kb/reingest

Backend selection is stored per organization and applies immediately.

------------------------------------------------------------------------

# Re-ingesting the Knowledge Base

Re-ingestion is required when:

-   Adding or modifying KB files
-   Changing backend
-   Updating supported device scope

Admin UI button:

**Re-ingest Knowledge Base**

API:

    POST /api/admin/kb/reingest

Re-ingestion:

-   Traverses `/knowledge`
-   Parses markdown
-   Chunks content
-   Generates embeddings
-   Populates selected vector table

------------------------------------------------------------------------

# Escalation Logic

Pin escalates automatically when:

-   Device type unsupported
-   OS unsupported
-   Application unsupported
-   No sufficient KB match found
-   User explicitly requests escalation

This prevents hallucinated support and enforces scope control.

------------------------------------------------------------------------

# Deployment

## Requirements

-   Python 3.10+
-   SQLite
-   sqlite-vec extension
-   Optional: Gemini API key

------------------------------------------------------------------------

## Install

    git clone https://github.com/joshsimp-uw/Pin.git
    cd Pin
    make install

------------------------------------------------------------------------

## Run

    uvicorn app.main:app --host 0.0.0.0 --port 8000

Access:

    http://<server>:8000

------------------------------------------------------------------------

# Environment Configuration

Create a `.env` file in project root.

## `.env.example`

    # Server
    HOST=0.0.0.0
    PORT=8000

    # Database
    DATABASE_PATH=data/pin.db

    # Admin
    ADMIN_TOKEN=change_this_to_secure_value

    # Gemini (optional)
    GEMINI_API_KEY=

    # Default RAG Backend
    DEFAULT_RAG_BACKEND=local

Notes:

-   If `GEMINI_API_KEY` is empty, system defaults to Local backend.
-   Backend can still be switched via Admin UI.

------------------------------------------------------------------------

# Database Tables (RAG)

Local embeddings:

    kb_vec_local

Gemini embeddings:

    kb_vec_gemini

Both tables may coexist. Switching does not require schema changes.

------------------------------------------------------------------------

# Production Hardening Recommendations

## 1. Reverse Proxy

Use:

-   Nginx
-   Caddy
-   Traefik

Terminate TLS at proxy and forward to uvicorn internally.

## 2. TLS

Use valid certificates (Let's Encrypt or internal PKI).

Never expose plain HTTP publicly.

## 3. Secure Admin Token

-   Change `ADMIN_TOKEN`
-   Store securely
-   Do not commit real tokens to repo

## 4. Restrict Network Access

If internal-only:

-   Bind to private IP
-   Restrict firewall to trusted subnets
-   Place behind VPN if needed

## 5. Disable Gemini in Restricted Environments

If operating air-gapped:

-   Ensure `GEMINI_API_KEY` is unset
-   Use local backend only

## 6. Regular Backups

Back up:

-   SQLite database
-   `/knowledge` directory

------------------------------------------------------------------------

# Development Notes

-   Backend selection is per-organization.
-   Vector tables are created automatically if missing.
-   Metadata inferred from folder path:
    -   category → device/os/application
    -   service → application
    -   tags → device, OS, application
-   Front-matter overrides supported.

------------------------------------------------------------------------

# Project Intent

Pin is built to:

-   Reduce helpdesk workload
-   Enforce supported device boundaries
-   Provide deterministic troubleshooting
-   Operate fully offline if required
-   Escalate cleanly when out-of-scope
