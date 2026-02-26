#!/usr/bin/env bash
set -euo pipefail

# Pin update script (manual run)
#
# This is the recommended operational command for keeping a deployment current:
#   make update
#
# (The older name `pin-nightly-update.sh` is retained as a compatibility wrapper.)

REPO_DIR="/projects/Pin"
BACKUP_ROOT="/projects/backup/Pin"
VENV_DIR="/projects/.pin-venv"
PIN_USER="pin"
SERVICE="pin.service"

DEMO_DB="${REPO_DIR}/demo/data/pin.demo.db"
LIVE_DB="${REPO_DIR}/data/pin.db"

DEMO_KB="${REPO_DIR}/demo/knowledge"
LIVE_KB="${REPO_DIR}/knowledge"

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="${BACKUP_ROOT}/${STAMP}"

log(){ echo "[$(date --iso-8601=seconds)] $*"; }

log "=== Pin update starting ==="

# 1) Backup
log "Backing up ${REPO_DIR} -> ${BACKUP_DIR}"
mkdir -p "${BACKUP_DIR}"
rsync -aH --delete \
  --exclude ".git" \
  --exclude "__pycache__" \
  --exclude "*.pyc" \
  "${REPO_DIR}/" "${BACKUP_DIR}/"

# 2) Stop service
log "Stopping ${SERVICE}"
systemctl stop "${SERVICE}" || true

# 3) Update repo
if [ -d "${REPO_DIR}/.git" ]; then
  log "Updating git repo..."
  cd "${REPO_DIR}"
  git fetch --all --prune
  git checkout main
  git pull --ff-only
else
  log "WARNING: ${REPO_DIR} is not a git checkout; skipping git pull."
fi

# 4) OS deps
log "Ensuring OS dependencies..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y >/dev/null
apt-get install -y \
  python3 python3-venv python3-pip \
  sqlite3 rsync git curl \
  build-essential libffi-dev libssl-dev >/dev/null

# 5) Venv + pip deps (persistent)
log "Ensuring venv at ${VENV_DIR}"
if [ ! -x "${VENV_DIR}/bin/python" ]; then
  python3 -m venv "${VENV_DIR}"
fi
"${VENV_DIR}/bin/python" -m pip install --upgrade pip wheel setuptools >/dev/null
"${VENV_DIR}/bin/python" -m pip install -r "${REPO_DIR}/requirements.txt" >/dev/null

# 6) Restore demo DB/KB
log "Restoring demo DB -> live DB"
if [ ! -f "${DEMO_DB}" ]; then
  log "ERROR: Demo DB missing: ${DEMO_DB}"
  exit 1
fi
mkdir -p "${REPO_DIR}/data"
cp -f "${DEMO_DB}" "${LIVE_DB}"
chown "${PIN_USER}:${PIN_USER}" "${LIVE_DB}" || true

log "Restoring demo knowledge -> live knowledge"
if [ -d "${DEMO_KB}" ]; then
  mkdir -p "${LIVE_KB}"
  rsync -a --delete "${DEMO_KB}/" "${LIVE_KB}/"
else
  log "WARNING: Demo knowledge folder missing: ${DEMO_KB}"
fi
chown -R "${PIN_USER}:${PIN_USER}" "${LIVE_KB}" || true

# 7) Rebuild KB index
log "Rebuilding KB index..."
rm -f "${REPO_DIR}/data/rag_index.pkl"
cd "${REPO_DIR}"
"${VENV_DIR}/bin/python" scripts/ingest_kb.py

# 8) Start service + health check
log "Starting ${SERVICE}"
systemctl start "${SERVICE}"
sleep 2
curl -fsS "http://127.0.0.1:8000/health" >/dev/null \
  && log "Health OK" \
  || log "Health check failed (see journalctl)."

log "=== Pin update finished ==="
