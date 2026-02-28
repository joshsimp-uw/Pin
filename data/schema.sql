PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;

-- Departments
CREATE TABLE IF NOT EXISTS departments (
  dept_id     INTEGER PRIMARY KEY,
  dept_name   TEXT NOT NULL UNIQUE
);

-- Organization (single-tenant: typically 1 row per DB)
CREATE TABLE IF NOT EXISTS orgs (
  org_id            TEXT PRIMARY KEY,
  name              TEXT NOT NULL,
  address           TEXT,
  city              TEXT,
  state             TEXT,
  zip               TEXT,
  poc_user_id       TEXT,
  tech_contact_user_id TEXT,
  created_at        TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (poc_user_id) REFERENCES users(user_id) ON DELETE SET NULL,
  FOREIGN KEY (tech_contact_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Users
CREATE TABLE IF NOT EXISTS users (
  user_id       TEXT PRIMARY KEY,
  org_id        TEXT NOT NULL,
  first_name    TEXT,
  last_name     TEXT,
  email         TEXT,
  role          TEXT NOT NULL DEFAULT 'end_user', -- end_user|admin|agent
  is_disabled   INTEGER NOT NULL DEFAULT 0, -- 0=active, 1=disabled (historical data retained)
  disabled_at   TEXT,
  dept_id       INTEGER,
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE,
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_users_org ON users(org_id);
CREATE INDEX IF NOT EXISTS idx_users_dept ON users(dept_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- User authentication (passwords)
-- NOTE: Passwords are stored as PBKDF2-HMAC-SHA256 hashes with per-user salt.
CREATE TABLE IF NOT EXISTS user_auth (
  user_id        TEXT PRIMARY KEY,
  password_salt  BLOB NOT NULL,
  password_hash  BLOB NOT NULL,
  algo           TEXT NOT NULL DEFAULT 'pbkdf2_sha256',
  updated_at     TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Auth sessions (simple bearer tokens)
CREATE TABLE IF NOT EXISTS auth_sessions (
  token       TEXT PRIMARY KEY,
  user_id     TEXT NOT NULL,
  org_id      TEXT NOT NULL,
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  expires_at  TEXT,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_auth_sessions_user ON auth_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_auth_sessions_org ON auth_sessions(org_id);

-- App configuration (per-org)
CREATE TABLE IF NOT EXISTS app_settings (
  org_id     TEXT NOT NULL,
  key        TEXT NOT NULL,
  value_json TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (org_id, key),
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_app_settings_org ON app_settings(org_id);

-- LLM provider configuration.
-- Store provider-specific API keys encrypted at rest.
CREATE TABLE IF NOT EXISTS llm_providers (
  org_id          TEXT NOT NULL,
  provider        TEXT NOT NULL, -- mock|openai|gemini
  model           TEXT NOT NULL,
  api_key_enc     TEXT,          -- encrypted (Fernet) + base64
  updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (org_id, provider),
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_llm_providers_org ON llm_providers(org_id);

-- Assets (generalized asset record)
CREATE TABLE IF NOT EXISTS assets (
  asset_id        TEXT PRIMARY KEY,
  org_id          TEXT NOT NULL,
  asset_type      TEXT NOT NULL,        -- laptop|desktop|mobile|printer|network|other
  vendor          TEXT,
  model           TEXT,
  date_acquired   TEXT,
  date_retired    TEXT,
  warranty_end    TEXT,
  properties_json TEXT NOT NULL DEFAULT '{}',
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_assets_org ON assets(org_id);
CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(asset_type);

-- Devices (operational/IT view; asset_tag is the primary key as requested)
CREATE TABLE IF NOT EXISTS devices (
  asset_tag        TEXT PRIMARY KEY,
  org_id           TEXT NOT NULL,
  asset_id         TEXT,                -- optional link to assets
  assigned_user_id TEXT,
  hostname         TEXT,
  serial_number    TEXT,
  os               TEXT,
  last_seen_at     TEXT,
  notes            TEXT,
  created_at       TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE,
  FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE SET NULL,
  FOREIGN KEY (assigned_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_devices_org ON devices(org_id);
CREATE INDEX IF NOT EXISTS idx_devices_user ON devices(assigned_user_id);
CREATE INDEX IF NOT EXISTS idx_devices_asset ON devices(asset_id);

-- Sessions (chat sessions)
CREATE TABLE IF NOT EXISTS sessions (
  session_id           TEXT PRIMARY KEY,
  org_id               TEXT NOT NULL,
  user_id              TEXT NOT NULL,
  title                TEXT,                       -- UI-facing summary/name
  ticket_id            TEXT,                       -- optional association to a ticket
  turns                INTEGER NOT NULL,
  category             TEXT,
  status               TEXT NOT NULL DEFAULT 'open', -- open|closed
  collected_json       TEXT NOT NULL,
  steps_attempted_json TEXT NOT NULL,
  created_at           TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at           TEXT NOT NULL DEFAULT (datetime('now')),
  closed_at            TEXT,
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_sessions_org_status ON sessions(org_id, status);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_ticket ON sessions(ticket_id);

-- Messages (chat transcript)
CREATE TABLE IF NOT EXISTS messages (
  message_id     TEXT PRIMARY KEY,
  session_id     TEXT NOT NULL,
  role           TEXT NOT NULL, -- user|assistant|system
  content        TEXT NOT NULL,
  citations_json TEXT NOT NULL DEFAULT '[]',
  created_at     TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_messages_session_time ON messages(session_id, created_at);

-- Tickets (escalations)
CREATE TABLE IF NOT EXISTS tickets (
  ticket_id            TEXT PRIMARY KEY,
  org_id               TEXT NOT NULL,
  user_id              TEXT NOT NULL, -- requester
  session_id           TEXT,
  summary              TEXT NOT NULL,
  category             TEXT NOT NULL,
  impact               TEXT NOT NULL DEFAULT 'medium',  -- low|medium|high
  urgency              TEXT NOT NULL DEFAULT 'medium',  -- low|medium|high
  status               TEXT NOT NULL DEFAULT 'created', -- created|closed
  escalation_reason    TEXT NOT NULL,
  rendered_text        TEXT NOT NULL,
  diagnostics_json     TEXT NOT NULL DEFAULT '{}',
  steps_attempted_json TEXT NOT NULL DEFAULT '[]',
  citations_json       TEXT NOT NULL DEFAULT '[]',
  created_at           TEXT NOT NULL DEFAULT (datetime('now')),
  closed_at            TEXT,
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_tickets_org_status ON tickets(org_id, status);
CREATE INDEX IF NOT EXISTS idx_tickets_session ON tickets(session_id);

-- ==============================
-- Knowledge Base (RAG)
-- ==============================

-- Document-level metadata
CREATE TABLE IF NOT EXISTS kb_documents (
  doc_id         TEXT PRIMARY KEY,
  category       TEXT NOT NULL,          -- folder name (iam, email, remote_access, ...)
  title          TEXT NOT NULL,
  service        TEXT,
  tags_json      TEXT NOT NULL DEFAULT '[]',
  source_path    TEXT NOT NULL,
  updated_at     TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_kb_documents_category ON kb_documents(category);

-- Chunked text (what we actually stuff into the LLM prompt)
CREATE TABLE IF NOT EXISTS kb_chunks (
  chunk_id       TEXT PRIMARY KEY,
  doc_id         TEXT NOT NULL,
  section_title  TEXT NOT NULL,
  heading_path   TEXT NOT NULL DEFAULT '',
  text           TEXT NOT NULL,
  updated_at     TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (doc_id) REFERENCES kb_documents(doc_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_kb_chunks_doc ON kb_chunks(doc_id);

-- Small key/value state table for KB ingestion + vector sync.
-- This lets us detect KB filesystem changes and rebuild embeddings automatically.
CREATE TABLE IF NOT EXISTS kb_state (
  key        TEXT PRIMARY KEY,
  value_text TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Vector indexes (sqlite-vec). These are virtual tables.
-- NOTE: This requires sqlite-vec extension to be loaded in the SQLite connection.
-- We maintain two indexes so admins can switch between an offline/local embedding
-- backend and Gemini embeddings without redeploying.
--
-- Local/offline backend (feature hashing). Dim matches TIER1_RAG_EMBEDDING_DIM_LOCAL.
CREATE VIRTUAL TABLE IF NOT EXISTS kb_vec_local USING vec0(
  chunk_id TEXT PRIMARY KEY,
  embedding float[384] distance_metric=cosine
);
-- Gemini embeddings backend. Dim matches TIER1_RAG_EMBEDDING_DIM_GEMINI.
CREATE VIRTUAL TABLE IF NOT EXISTS kb_vec_gemini USING vec0(
  chunk_id TEXT PRIMARY KEY,
  embedding float[3072] distance_metric=cosine
);
