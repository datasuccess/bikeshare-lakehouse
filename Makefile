# Makefile — the single documented command interface for the repo.
# Purpose: one place to run everything; `make` (or `make help`) lists targets.
# Why: reviewers and future-me should never have to guess the commands (docs/05-conventions.md).
# Note: some targets reference files that land in later phases (infra/, dbt/, tests/) — they define
#       the intended interface now and become live as those phases are built.

.DEFAULT_GOAL := help

# --- Environment -------------------------------------------------------------
setup:            ## install pinned dev deps into .venv (uv)
	uv sync

# --- Local stack (Phase 0 build: infra/docker-compose.local.yml) --------------
up:               ## start the local stack (MinIO + Postgres + Airflow + catalog)
	docker compose -f infra/docker-compose.local.yml up -d

down:             ## stop the local stack
	docker compose -f infra/docker-compose.local.yml down

# --- Pipeline (Phases 1-6) ---------------------------------------------------
run:              ## ingest -> vault -> marts -> data quality (end to end)
	@echo "not yet implemented — lands with Phases 1-6 (see docs/04-roadmap.md)"

# --- Quality -----------------------------------------------------------------
lint:             ## ruff + sqlfluff (sqlfluff activates once dbt/ exists)
	uv run ruff check .

fmt:              ## auto-format Python
	uv run ruff format .

test:             ## run pytest
	uv run pytest

hooks:            ## run all pre-commit hooks over the repo
	uv run pre-commit run --all-files

# --- Housekeeping ------------------------------------------------------------
clean:            ## remove generated data + local lake + duckdb (safe; regenerable)
	rm -rf data/ bronze/ silver/ gold/ *.duckdb *.duckdb.wal dbt/target dbt/logs

help:             ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

.PHONY: setup up down run lint fmt test hooks clean help
