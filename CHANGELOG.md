# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · Versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Added
- **Phase 2 — lakehouse landing:** Iceberg **REST catalog** in the local stack (`apache/iceberg-rest-fixture`)
  + `lakehouse/` package (pure Bronze→Arrow parsers; idempotent `land` into partitioned Iceberg tables
  `raw_station_status` / `raw_station_information` / `raw_trips`; `python -m lakehouse land` CLI, `make land`).
  Unit tests via pyiceberg's SQLite catalog (no Docker). Docs: `lakehouse/LEARNING.md`. Deps: `pyiceberg`, `pyarrow`.
- **Phase 1 — ingestion:** local MinIO stack (`infra/docker-compose.local.yml`) + `ingestion/` package
  (GBFS discovery/snapshot loader, historical trip-file loader, resilient HTTP with 429/5xx backoff,
  env-driven S3/MinIO storage, `python -m ingestion` CLI). Unit tests (mocked API + in-memory store);
  ruff + pytest wired into CI. Docs: `DATA_SOURCES` (Capital Bikeshare), `LEARNING_GUIDE`, `GLOSSARY`,
  and `ingestion/LEARNING.md`.
- **Phase 0 — scaffold:** repo structure, docs (overview, architecture, ADRs, data model, roadmap,
  conventions, cost, case study), per-component purpose READMEs, and hygiene (LICENSE, `.gitignore`,
  `.env.example`, pre-commit, CI secret-scan + hygiene, SECURITY).
- **Phase 0.5 — engineering foundation:** `uv` project (`pyproject.toml` + lockfile) + `.python-version`,
  `Makefile`, dev container, `.editorconfig` / `.gitattributes`, lint configs (`.sqlfluff`, `.yamllint`),
  Dependabot, PR/issue templates, `CODEOWNERS`, `CONTRIBUTING`, and `docs/DATA_SOURCES.md`.

<!-- Each phase adds an entry here as it merges. First tagged release: after the local pipeline
     (Phases 1-7) runs end to end. -->
