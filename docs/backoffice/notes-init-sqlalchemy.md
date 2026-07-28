# SQLAlchemy setup — backoffice notes

Notes taken while wiring SQLAlchemy into the Flask backoffice. Meant to help
teammates understand the setup, not as a launch guide (see the README for that).

## Dependencies
Two packages are needed to talk to MySQL:
- **SQLAlchemy** — the ORM; simplifies building and running queries.
- **PyMySQL** — the driver that actually "speaks" to MySQL. SQLAlchemy does not
  talk to any database on its own; it needs a driver. PyMySQL is pure Python, so
  it installs with no system dependencies (unlike mysqlclient, which is compiled).
  The driver appears in the connection URL: `mysql+pymysql://...`.

## Three core objects
- **engine**: the connection point to the database. Holds the URL
  (`mysql+pymysql://...`) and manages the connection pool. Created once at startup.
  It does not connect immediately — the real connection opens on first use (lazy).
- **session**: the workspace for a set of operations (read/write). We want one
  session per HTTP request.
- **Base**: the parent class all models inherit from. Holds the registry of tables
  used by `create_all()`.

## Session lifecycle and teardown
- `scoped_session` (in database.py) provides one session per context automatically,
  so we don't have to pass the session around manually.
- **teardown** (Flask term = "cleanup at the end"): Flask runs a registered function
  at the end of every request, even if it failed. We use it to close the session
  (`SessionLocal.remove()`), avoiding leaked connections. Conceptually similar to a
  Python `with` block — guaranteed cleanup.

## Checking DB connectivity without models
To confirm the app connects to the DB before any model exists, `/health` runs a
`SELECT 1`:
- it is the lightest possible query and depends on no table, so it tests only the
  connection (URL + driver + credentials + network).
- the route opens a session and runs `SELECT 1`; the session is closed automatically
  by the teardown, not in the route.

Once running:
```bash
curl -i http://localhost:8080/health
```
Response: