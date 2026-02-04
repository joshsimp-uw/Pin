# Database

Pin uses SQLite for persistence. In production-like deployments, **each organization gets its own SQLite file**
(e.g., `data/pin.db` located on that org's site/server).

## Files

- `data/schema.sql` — authoritative schema
- `app/core/db.py` — connection + schema initialization
- `app/core/session.py` — session persistence helpers
- `app/core/repository.py` — common insert/query helpers (org/user/messages/tickets)

## Configuration

SQLite path is controlled by:

- `TIER1_SQLITE_PATH` (env var)
- default: `data/pin.db`

Example:

```bash
export TIER1_SQLITE_PATH=/var/pin/acme/pin.db
```

## Initialization

The API calls `init_schema()` on startup to ensure tables exist. For new org deployments, you can also run:

```bash
python scripts/create_empty_db.py --db data/pin.db --schema data/schema.sql
```

## Seeding test data

```bash
python scripts/create_test_db.py --db data/pin_test.db --schema data/schema.sql
```

## Integrity notes (single-tenant org DB)

Even though each DB is single-tenant, tables still keep an `org_id` column. This makes:
- demo data clearer
- future multi-tenant refactors easier
- API filtering explicit

Foreign keys are enabled (`PRAGMA foreign_keys=ON`) on every connection.
