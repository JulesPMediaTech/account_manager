# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A Flask web application for user account management with role-based access control, PostgreSQL backend, and Docker deployment. It provides a GUI for creating, editing, deactivating, and deleting user accounts.

## Commands

### Install Dependencies
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Run (Development)
```bash
python server.py  # runs on localhost
```

### Viewing and Feedback
Claude Chrome extension is installed and enabled. Report any issues.
Access:
local: http://localhost
remote with ssl: https://modernaccess.duckdns.org:4443


### Run (Docker / Production Stack)
```bash
docker-compose up -d          # starts Flask app, PostgreSQL, Nginx, Certbot
docker-compose -f docker-compose.test.yml up  # testing stack
```

### Database Migrations
```bash
flask db migrate -m "description"
flask db upgrade
```

### Tests
```bash
pytest tests/ -v              # all tests
pytest tests/test_auth.py -v  # single test file
pytest tests/test_auth.py::test_login_valid -v  # single test
```

## Architecture

**App Factory:** `app/__init__.py` exports `create_app()`, which wires together extensions, blueprints, error handlers, and config. Use this pattern when adding new extensions.

**Blueprints:**
- `app/routes/auth.py` — login/logout (`/login`, `/logout`)
- `app/routes/main.py` — all user management routes (`/add_user`, `/show_user_table`, `/edit_user`, `/delete_user`, `/change_password`, `/deactivate_user`)

**Extensions** (`app/extensions.py`): `db`, `migrate`, `login_manager` are instantiated here and initialized in `create_app()`. Import extensions from this module to avoid circular imports.

**Database Layer** (`app/db.py`): `UserDatabase` class wraps all SQLAlchemy operations. Routes call methods on this class rather than querying directly. The `User` model lives in `app/models.py`.

**Role System** (`app/roles.py`): Roles are grouped into `staffers`, `members`, `paid`, `inactive`, and `all`. The `@roles_required(*roles)` decorator in `app/custom_decorators.py` enforces access at the route level.

**Configuration** (`app/config.py`): Secrets are read from Docker secrets files (`/run/secrets/`) with fallback to environment variables. The `.secrets/` directory holds local dev secrets. Tests override config via `TESTING=True` and use SQLite in-memory.

**Forms** (`app/forms.py`): WTForms with CSRF protection. Three forms: `LoginForm`, `UserForm` (create/edit), `DeactivateUserForm`.

## Key Conventions

- Tests use an in-memory SQLite DB and disable CSRF; fixtures are in `tests/conftest.py`.
- Docker secrets are preferred over `.env` for production credentials (`SECRET_KEY`, `DB_PASSWORD`).
- The `deactivate_user` operation sets a user's role to `disabled` or `banned` rather than deleting them.
- `wsgi.py` is the Waitress entry point used inside Docker; `server.py` is for local dev.

## SQL Table Data

Current data is fictitious. Passwords are deliberately simple for dev usage. 
Errors shown explicitly for dev.