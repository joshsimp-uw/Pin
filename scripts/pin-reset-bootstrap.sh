#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/projects/Pin"
SERVICE="pin.service"

log(){ echo "[$(date --iso-8601=seconds)] $*"; }

log "Stopping ${SERVICE}"
systemctl stop "${SERVICE}" || true

log "Removing live DB and indexes"
rm -f "${REPO_DIR}/data/pin.db"
rm -f "${REPO_DIR}/data/rag_index.pkl"

# Optional: remove encryption key to force new one on next init
rm -f "${REPO_DIR}/data/secret.key"

log "Clearing knowledge folder (optional — comment out if you want KB retained)"
rm -rf "${REPO_DIR}/knowledge"
mkdir -p "${REPO_DIR}/knowledge"

log "Starting ${SERVICE}"
systemctl start "${SERVICE}"

log "Reset complete. App should present setup/bootstrap flow."