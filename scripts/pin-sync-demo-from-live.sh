#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

LIVE_DB="${REPO_DIR}/data/pin.db"
DEMO_DB="${REPO_DIR}/demo/data/pin.demo.db"

LIVE_KB="${REPO_DIR}/knowledge"
DEMO_KB="${REPO_DIR}/demo/knowledge"

log(){ echo "[$(date --iso-8601=seconds)] $*"; }

mkdir -p "${REPO_DIR}/demo/data"
mkdir -p "${REPO_DIR}/demo/knowledge"

log "Copying live DB -> demo DB"
cp -f "${LIVE_DB}" "${DEMO_DB}"

log "Sanitizing demo DB (removing encrypted API keys)"
sqlite3 "${DEMO_DB}" <<'SQL'
UPDATE llm_providers SET api_key_enc = NULL;
SQL

log "Copying live knowledge -> demo knowledge"
rsync -a --delete "${LIVE_KB}/" "${DEMO_KB}/"

log "Done. Demo is refreshed (and secrets scrubbed)."