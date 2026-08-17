# Contributing

> **Purpose:** how to work in this repo. It's primarily a solo, education-first portfolio project, but
> the workflow is run like a real team's — that discipline is part of the point.

## Setup
```bash
uv sync                 # install pinned dev deps (needs uv + Python 3.12)
uv run pre-commit install
make help               # see all commands
```
Or open in **GitHub Codespaces / VS Code Dev Containers** — the `.devcontainer/` sets everything up.

## Workflow (non-negotiable — see docs/05-conventions.md)
1. **One phase / concern per branch.** Branch from `main`: `feat/…`, `fix/…`, `docs/…`, `chore/…`.
2. **Pre-discuss scope + real decisions** before coding (add an ADR to `docs/02-decisions.md` if a
   real decision is made).
3. Build → **test locally** (`make hooks`, `make test`) → open a **PR** → **CI green** → merge.
4. Never push big work straight to `main` (it's protected).
5. Every new/changed source file carries the **purpose header**; every phase ships a `LEARNING.md`.

## Commits
- **Conventional Commits**: `feat: …`, `fix: …`, `docs: …`, `chore: …`, `ci: …`, `test: …`.
- **No AI co-authorship trailers.** Sole author is the repo owner.
- **No secrets, no PII, no generated data** committed (`.gitignore` + gitleaks enforce this).

## Definition of done
A change is done when it runs from a documented command, is tested, is documented, and CI is green.
