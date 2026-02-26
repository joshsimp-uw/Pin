#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

LIVE_DB="${REPO_DIR}/data/pin.db"
DEMO_DB="${REPO_DIR}/demo/data/pin.demo.db"

LIVE_KB="${REPO_DIR}/knowledge"
DEMO_KB="${REPO_DIR}/demo/knowledge"

log(){ echo "[$(date --iso-8601=seconds)] $*"; }

# --- Sanity checks
if [ ! -f "${LIVE_DB}" ]; then
  echo "ERROR: live DB not found: ${LIVE_DB}"
  exit 1
fi

mkdir -p "${REPO_DIR}/demo/data"
mkdir -p "${REPO_DIR}/demo/knowledge"

# --- Copy live DB -> demo DB
log "Copying live DB -> demo DB"
cp -f "${LIVE_DB}" "${DEMO_DB}"

# --- Scrub secrets from demo DB
# Keep demo users, roles, settings; remove encrypted API keys (and any other sensitive values you add later)
log "Sanitizing demo DB (removing encrypted API keys)"
sqlite3 "${DEMO_DB}" <<'SQL'
-- Remove stored encrypted API keys (prevent committing secrets)
UPDATE llm_providers SET api_key_enc = NULL;

-- Optional: force demo to always require setup on restore:
-- UPDATE app_settings SET value='false' WHERE key='initialized';

-- Optional: if you store tokens/sessions in DB in the future, wipe them:
-- DELETE FROM sessions;
SQL

# --- Copy knowledge base -> demo knowledge
if [ -d "${LIVE_KB}" ]; then
  log "Copying live knowledge -> demo knowledge"
  rsync -a --delete "${LIVE_KB}/" "${DEMO_KB}/"
else
  log "WARNING: live knowledge folder missing: ${LIVE_KB} (skipping)"
fi

# --- Guardrails: ensure we don't accidentally stage runtime secrets
log "Prep complete."
log "Next:"
log "  git status"
log "  (verify demo/data/pin.demo.db and demo/knowledge/* only)"