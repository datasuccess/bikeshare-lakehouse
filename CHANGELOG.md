# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · Versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Added
- **Phase 0 — scaffold:** repo structure, docs (overview, architecture, ADRs, data model, roadmap,
  conventions, cost, case study), per-component purpose READMEs, and hygiene (LICENSE, `.gitignore`,
  `.env.example`, pre-commit, CI secret-scan + hygiene, SECURITY).
- **Phase 0.5 — engineering foundation:** `uv` project (`pyproject.toml` + lockfile) + `.python-version`,
  `Makefile`, dev container, `.editorconfig` / `.gitattributes`, lint configs (`.sqlfluff`, `.yamllint`),
  Dependabot, PR/issue templates, `CODEOWNERS`, `CONTRIBUTING`, and `docs/DATA_SOURCES.md`.

<!-- Each phase adds an entry here as it merges. First tagged release: after the local pipeline
     (Phases 1-7) runs end to end. -->
