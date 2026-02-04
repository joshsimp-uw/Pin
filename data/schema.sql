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
  dept_id       INTEGER,
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE,
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_users_org ON users(org_id);
CREATE INDEX IF NOT EXISTS idx_users_dept ON users(dept_id);

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

-- Sessions (extends current implementation; links to org/user)
CREATE TABLE IF NOT EXISTS sessions (
  session_id           TEXT PRIMARY KEY,
  org_id               TEXT NOT NULL,
  user_id              TEXT NOT NULL,
  turns                INTEGER NOT NULL,
  category             TEXT,
  status               TEXT NOT NULL DEFAULT 'open', -- open|closed
  collected_json       TEXT NOT NULL,
  steps_attempted_json TEXT NOT NULL,
  created_at           TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at           TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_sessions_org_status ON sessions(org_id, status);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);

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
