#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PIN_USER="${PIN_USER:-pin}"
SERVICE_NAME="${SERVICE_NAME:-pin.service}"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}"

VENV_DIR="${REPO_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

DEMO_DB="${REPO_DIR}/demo/data/pin.demo.db"
LIVE_DB="${REPO_DIR}/data/pin.db"
DEMO_KB="${REPO_DIR}/demo/knowledge"
LIVE_KB="${REPO_DIR}/knowledge"

log(){ echo "[$(date --iso-8601=seconds)] $*"; }

require_root() {
  if [ "$(id -u)" -ne 0 ]; then
    echo "Run as root: sudo $0"
    exit 1
  fi
}

ensure_user() {
  if id "${PIN_USER}" >/dev/null 2>&1; then
    log "User '${PIN_USER}' exists."
  else
    log "Creating user '${PIN_USER}'..."
    useradd --system --create-home --shell /usr/sbin/nologin "${PIN_USER}"
  fi
}

install_os_deps() {
  log "Installing OS dependencies..."
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y >/dev/null
  apt-get install -y \
    "${PYTHON_BIN}" python3-venv python3-pip \
    sqlite3 rsync curl \
    build-essential libffi-dev libssl-dev \
    >/dev/null
}

create_dirs() {
  log "Ensuring required directories exist..."
  mkdir -p "${REPO_DIR}/data"
  mkdir -p "${LIVE_KB}"

  # Runtime env (secrets/config). Not overwritten if it already exists.
  mkdir -p /etc/pin
  if [ ! -f /etc/pin/pin.env ]; then
    cat > /etc/pin/pin.env <<ENVEOF
# Pin service configuration (Environment variables are prefixed with TIER1_)
# Example:
# TIER1_ENVIRONMENT=prod
# TIER1_ADMIN_TOKEN=change-me
# TIER1_CORS_ORIGINS=https://pin.example.com
# TIER1_DEMO_SEED=false
# TIER1_SESSION_TTL_SECONDS=28800
# Crypto
# TIER1_SECRET_KEY=<urlsafe base64 32-byte key>  # master key used to encrypt stored provider API keys
ENVEOF
    chmod 600 /etc/pin/pin.env
  fi

  # Ensure the master encryption key exists (KEK pattern). This key is used to
  # encrypt provider API keys stored in the DB. We keep it outside the repo and
  # load it via systemd EnvironmentFile.
  if ! grep -qE '^\s*TIER1_SECRET_KEY=' /etc/pin/pin.env; then
    log "Generating TIER1_SECRET_KEY and writing to /etc/pin/pin.env ..."
    SECRET_KEY="$(${PYTHON_BIN} - <<'PY'
import base64, os
print(base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8'))
PY
)"
    echo "TIER1_SECRET_KEY=${SECRET_KEY}" >> /etc/pin/pin.env
    chmod 600 /etc/pin/pin.env
  else
    log "TIER1_SECRET_KEY already present in /etc/pin/pin.env"
  fi

  chown -R "${PIN_USER}:${PIN_USER}" "${REPO_DIR}/data" || true
  chown -R "${PIN_USER}:${PIN_USER}" "${LIVE_KB}" || true
}

create_venv_and_install() {
  log "Creating/updating venv at ${VENV_DIR}..."
  if [ ! -x "${VENV_DIR}/bin/python" ]; then
    sudo -u "${PIN_USER}" "${PYTHON_BIN}" -m venv "${VENV_DIR}"
  fi

  log "Installing python requirements..."
  sudo -u "${PIN_USER}" "${VENV_DIR}/bin/python" -m pip install --upgrade pip wheel setuptools >/dev/null
  sudo -u "${PIN_USER}" "${VENV_DIR}/bin/python" -m pip install -r "${REPO_DIR}/requirements.txt"
}

restore_demo_state_if_present() {
  # Optional but recommended for your demo workflow.
  if [ -f "${DEMO_DB}" ]; then
    log "Restoring demo DB -> ${LIVE_DB}"
    cp -f "${DEMO_DB}" "${LIVE_DB}"
    chown "${PIN_USER}:${PIN_USER}" "${LIVE_DB}" || true
  else
    log "No demo DB found at ${DEMO_DB}; leaving DB to be initialized by bootstrap flow."
  fi

  if [ -d "${DEMO_KB}" ]; then
    log "Restoring demo knowledge -> ${LIVE_KB}"
    rsync -a --delete "${DEMO_KB}/" "${LIVE_KB}/"
    chown -R "${PIN_USER}:${PIN_USER}" "${LIVE_KB}" || true
  else
    log "No demo knowledge folder found at ${DEMO_KB}; leaving knowledge as-is."
  fi
}

build_kb_index_if_possible() {
  # Only if the ingest script exists.
  if [ -f "${REPO_DIR}/scripts/ingest_kb.py" ]; then
    log "Building KB index..."
    rm -f "${REPO_DIR}/data/rag_index.pkl"
    sudo -u "${PIN_USER}" bash -lc "cd '${REPO_DIR}' && '${VENV_DIR}/bin/python' scripts/ingest_kb.py"
  else
    log "No scripts/ingest_kb.py found; skipping KB ingestion."
  fi
}

install_service() {
  log "Installing systemd service to ${SERVICE_PATH}..."

  cat > "${SERVICE_PATH}" <<EOF
[Unit]
Description=Pin FastAPI Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${PIN_USER}
WorkingDirectory=${REPO_DIR}
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=-/etc/pin/pin.env
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=strict
ReadWritePaths=${REPO_DIR}/data ${LIVE_KB}
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
ExecStart=${VENV_DIR}/bin/python -m uvicorn app.main:app --host ${HOST} --port ${PORT}
Restart=on-failure
RestartSec=3
TimeoutStopSec=30
KillSignal=SIGINT
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload
  systemctl enable "${SERVICE_NAME}"
}

start_service() {
  log "Starting ${SERVICE_NAME}..."
  systemctl restart "${SERVICE_NAME}"
  systemctl status "${SERVICE_NAME}" --no-pager || true

  log "Health check (if /health exists)..."
  sleep 2
  curl -fsS "http://127.0.0.1:${PORT}/health" >/dev/null && log "Health OK" || log "Health endpoint not responding (check journalctl)."
}

main() {
  require_root
  install_os_deps
  ensure_user
  create_dirs
  create_venv_and_install
  restore_demo_state_if_present
  build_kb_index_if_possible
  install_service
  start_service

  log "Install complete."
  log "Logs: sudo journalctl -u ${SERVICE_NAME} -n 200 --no-pager"
}

main "$@"