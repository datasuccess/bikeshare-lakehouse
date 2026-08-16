# Security policy

> **Purpose:** state how secrets and data are handled. This is a public, education-first repo — the
> bar is "nothing sensitive, ever."

## Secrets
- **Never committed.** `.env` is git-ignored; `.env.example` documents the variables with safe local
  defaults. Real credentials live only in an untracked `.env` (local) or CI/cloud secret stores.
- **Scanned** — `gitleaks` + `detect-private-key` run in pre-commit and CI (full history).
- **Cloud (later):** prefer OIDC / short-lived credentials; no long-lived keys in the repo or history.

## Data
- Only **public bike-share open data** (GBFS station/status + published trip files) is used.
- **No PII** — data is station- and trip-level; personal identifiers are not ingested or stored.
- Generated data and the local lake (`bronze/ silver/ gold/`, `*.duckdb`) are git-ignored and
  regenerable — never committed.

## Reporting
Found something sensitive committed by mistake? Open an issue (without disclosing the secret) or contact
the repo owner directly, and it will be rotated + purged from history.
