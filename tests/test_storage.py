# ── tests/test_storage.py ────────────────────────────────
# Purpose : the in-memory storage double behaves like the contract (put/exists/uri).
from __future__ import annotations

from ingestion.storage import InMemoryStorage


def test_put_and_exists():
    store = InMemoryStorage()
    assert store.exists("bronze/x") is False

    uri = store.put_bytes("bronze/x", b"hello")

    assert uri == "mem://bronze/x"
    assert store.exists("bronze/x") is True
    assert store.objects["bronze/x"] == b"hello"
