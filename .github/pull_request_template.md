<!-- Purpose: a consistent PR checklist that enforces the working agreement (docs/05-conventions.md). -->

## What & why
<!-- One or two sentences. Link the phase/issue and any ADR this touches. -->

Closes #

## Changes
-

## Checklist
- [ ] Scoped to one phase / concern
- [ ] New/changed source files carry the **purpose header** (docs/05-conventions.md)
- [ ] Tests added/updated (pytest / dbt / Soda) as appropriate
- [ ] Docs updated (README / docs / ADR added if a real decision was made)
- [ ] `make hooks` clean · CI green
- [ ] No secrets; no PII; no committed generated data
