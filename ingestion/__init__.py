# ── ingestion/__init__.py ────────────────────────────────
# Purpose : Phase 1 ingestion package — fetch real Capital Bikeshare data, land raw in Bronze.
# Why     : the pipeline's entry point; everything downstream reads what lands here (ADR-008).
# Docs    : docs/03-data-model.md · docs/DATA_SOURCES.md · ingestion/LEARNING.md
"""Ingestion: land raw GBFS snapshots and historical trip files into the Bronze zone."""

__all__ = ["__version__"]
__version__ = "0.1.0"
