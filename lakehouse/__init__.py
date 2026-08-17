# ── lakehouse/__init__.py ────────────────────────────────
# Purpose : Phase 2 — turn raw Bronze objects into Apache Iceberg tables on MinIO.
# Why     : a table format (Iceberg) gives raw files ACID, schema, snapshots and time-travel —
#           the "lakehouse" the Data Vault (Phase 3) then reads (docs/01-architecture.md).
# Docs    : lakehouse/LEARNING.md
"""Lakehouse landing: parse Bronze and append into Iceberg tables (the raw layer)."""

__all__ = ["__version__"]
__version__ = "0.1.0"
