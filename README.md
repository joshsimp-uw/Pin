# Pin -- Tier 0 / Tier 1 Support Assistant

Pin is a company-scoped **Tier 0 / Tier 1 IT support assistant**
designed to:

-   Collect structured troubleshooting data
-   Retrieve knowledge base documentation (RAG)
-   Provide grounded answers
-   Escalate to ticket when documentation confidence is low
-   Operate as a deployable system service

This project is built for real operational environments, not just local
demos.

------------------------------------------------------------------------

# Features

-   FastAPI backend with session state
-   Required-question gate (structured intake before troubleshooting)
-   RAG over markdown KB files
-   Ticket escalation when confidence is low
-   Pluggable LLM providers:
    -   Mock (offline deterministic)
    -   OpenAI-compatible
    -   Gemini
-   Encrypted per-LLM API key storage (Fernet)
-   Admin UI for LLM configuration
-   Bootstrap initialization flow
-   Demo state + runtime state separation
-   Systemd service support
-   Nightly rebuild automation
-   Makefile task orchestration

------------------------------------------------------------------------

# Architecture Overview

    app/
      core/        auth, crypto, config store, session state
      flows/       required-question engine
      rag/         TF-IDF retrieval
      llm/         provider abstraction
      policies/    escalation + guardrails
      models/      pydantic schemas

    knowledge/     live runtime KB
    demo/          version-controlled demo snapshot
    data/          runtime database + encryption key (ignored by git)
    scripts/       install + update + demo prep automation
    configs/       flow definitions

------------------------------------------------------------------------

# Installation (First-Time Setup)

``` bash
sudo ./scripts/install.sh
```

This will:

-   Install OS dependencies
-   Create `.venv`
-   Install Python requirements
-   Restore demo DB (if present)
-   Rebuild KB index
-   Install and enable `pin.service`
-   Start the API

Service runs on:

    http://localhost:8000

Check status:

``` bash
sudo systemctl status pin.service
```

View logs:

``` bash
sudo journalctl -u pin.service -n 200 --no-pager
```

------------------------------------------------------------------------

# Makefile Commands

Pin includes operational shortcuts:

``` bash
make prep         # Snapshot live state into demo/ (sanitized)
make install      # First-time setup
make nightly      # Run nightly update manually
make demo-reset   # Reset to bootstrap state
make health       # API health check
```

------------------------------------------------------------------------

# Demo Snapshot Workflow (Before Git Push)

Before committing changes:

``` bash
make prep
git status
git add .
git commit -m "Update demo snapshot + feature"
git push
```

`make prep`:

-   Copies live DB → demo DB
-   Removes encrypted API keys
-   Copies live KB → demo KB
-   Prevents secret leakage

------------------------------------------------------------------------

# Nightly Update Process

`scripts/pin-nightly-update.sh`:

1.  Backup `/projects/Pin`
2.  Pull latest repo
3.  Rebuild `.venv` dependencies
4.  Restore demo DB + KB
5.  Rebuild KB index
6.  Restart service
7.  Health check

This guarantees consistent demo state.

------------------------------------------------------------------------

# Bootstrap Mode

If no database exists, Pin routes to a setup page:

-   Create initial admin user
-   Select LLM provider
-   Store encrypted API key
-   Mark system initialized

------------------------------------------------------------------------

# LLM Configuration

LLMs are configured via Admin UI.

Supported providers:

-   mock
-   openai
-   gemini

Each provider:

-   Stores its own encrypted API key
-   Can be switched dynamically

Encryption:

-   Fernet symmetric encryption
-   Key stored in `data/secret.key`
-   Never committed to git

------------------------------------------------------------------------

# Knowledge Base (RAG)

Add markdown files to:

    knowledge/

Then rebuild index:

``` bash
python scripts/ingest_kb.py
```

------------------------------------------------------------------------

# Security Model

-   Encrypted API keys
-   Secrets excluded via `.gitignore`
-   Role-based admin access
-   No KB match → escalation
-   Guardrails against unsafe advice

------------------------------------------------------------------------

# Development Philosophy

Pin is built as:

-   A reproducible service
-   A company-scoped support assistant
-   A capstone-ready but production-minded project
-   A foundation for future enterprise integration (ITSM, OIDC, vector
    DB)

------------------------------------------------------------------------

# Future Enhancements

-   Replace TF-IDF with embeddings + vector DB
-   ITSM integration (ServiceNow / Jira / Zendesk)
-   Multi-org isolation
-   Audit logging
-   OIDC authentication
-   Automated test suite
