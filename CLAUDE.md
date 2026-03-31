# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```shell
# Install dependencies
uv sync --all-extras --dev

# Start local database + run migrations
docker compose up -d database database-migrations

# Run the API server locally (requires .env file)
uv run --env-file .env uvicorn myapi.main:app

# Run all tests (uses SQLite by default, no DB required)
uv run python -m pytest tests

# Run tests against a real PostgreSQL database
uv run python -m pytest tests --database-url postgresql+psycopg://user:pass@localhost/myapi

# Run a single test file
uv run python -m pytest tests/actors/test_actors_database.py

# Lint and format (via pre-commit)
pre-commit run --all-files
```

Linting uses **ruff** (import sorting + formatting) and **mypy** (type checking). Install hooks with `pre-commit install`.

## Architecture

The app (`myapi/`) has two parallel feature modules demonstrating sync vs async database access:

- `myapi/actors/` — synchronous CRUD endpoints at `/actors`, uses `psycopg` via SQLAlchemy sync sessions
- `myapi/async_actors/` — async CRUD endpoints at `/async/actors`, uses `asyncpg` via SQLAlchemy async sessions

Both modules follow the same internal structure: `router.py` → `service.py` (ABC interface) → `queries.py` (SQLAlchemy implementation) + `schemas.py` (Pydantic) + `exceptions.py`.

**Shared infrastructure** (`myapi/shared/`):
- `configuration.py` — reads DB config from environment variables (`DATABASE_HOST`, `DATABASE_USER`, `DATABASE_PASSWORD` required; `DATABASE_PORT`, `DATABASE_NAME` optional)
- `database/session.py` — `SQLAlchemySessionFactory` (sync, psycopg)
- `database/async_session.py` — `SQLAlchemyAsyncSessionFactory` (async, asyncpg)
- `database/models.py` — SQLAlchemy ORM model(s)
- `dependencies.py` — module-level singleton factories; FastAPI dependency functions `get_database_session` / `get_async_database_session`

Database migrations are managed with **Alembic** (config in `alembic.ini`, migrations in `myapi/_migrations/`).

The test suite uses SQLite in-memory by default (no running database needed). The `conftest.py` creates and tears down the SQLite file per session.
