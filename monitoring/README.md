# monitoring/ — observability & alerts

> **Purpose:** watch the platform from its own output — feed freshness, SLA, completeness — and alert
> on failure. **Status:** planned (Phase 8). Spec only.

## Planned contents
- `grafana/` — dashboards + SQL panels querying the warehouse's own tables: GBFS feed **freshness**,
  snapshot **completeness**, station **stock-out rate**, pipeline run duration / SLA.
- `alerts/` — failure + freshness-breach notifications (Slack / Telegram).

## Why this matters
"Monitored from its own output" is the senior differentiator — the platform reports on its own health,
not just whether a DAG turned green. Inspired by the cmc-crypto reference repo's Grafana + alerting.
