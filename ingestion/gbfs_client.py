# ── ingestion/gbfs_client.py ─────────────────────────────
# Purpose : discover GBFS feeds at runtime and land raw snapshots in Bronze.
# Why     : GBFS only serves "now" (ttl 60s). We snapshot it over time to BUILD the history the
#           source never keeps — the core Data Vault satellite story (ADR-008).
# Inputs  : GBFS discovery URL      Outputs: raw feed JSON at bronze/gbfs/<system>/<feed>/dt=.../...
# Docs    : docs/DATA_SOURCES.md · ingestion/LEARNING.md
from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING

import httpx

from . import _http

if TYPE_CHECKING:
    from .storage import Storage

_USER_AGENT = "bikeshare-lakehouse/0.1 (+https://github.com/datasuccess/bikeshare-lakehouse)"


class GbfsClient:
    """Reads a GBFS system: resolves feed URLs from the discovery doc, then fetches feeds."""

    def __init__(
        self,
        discovery_url: str,
        *,
        language: str = "en",
        client: httpx.Client | None = None,
        max_attempts: int = 5,
        backoff: float = 1.0,
    ) -> None:
        self._discovery_url = discovery_url
        self._language = language
        self._client = client or httpx.Client(timeout=15.0, headers={"User-Agent": _USER_AGENT})
        self._max_attempts = max_attempts
        self._backoff = backoff
        self._feeds: dict[str, str] | None = None

    def _get(self, url: str) -> httpx.Response:
        return _http.get(self._client, url, max_attempts=self._max_attempts, backoff=self._backoff)

    def discover(self, *, refresh: bool = False) -> dict[str, str]:
        """Return {feed_name: url}. Cached after first call (refresh=True to re-read)."""
        if self._feeds is None or refresh:
            data = self._get(self._discovery_url).json()["data"]
            feeds = data[self._language]["feeds"] if self._language in data else data["feeds"]
            self._feeds = {f["name"]: f["url"] for f in feeds}
        return self._feeds

    def fetch_feed_raw(self, name: str) -> bytes:
        """Fetch a feed's exact bytes (what we land in Bronze — immutable raw)."""
        feeds = self.discover()
        if name not in feeds:
            raise KeyError(f"GBFS feed {name!r} not available; have {sorted(feeds)}")
        return self._get(feeds[name]).content

    def fetch_feed(self, name: str) -> dict:
        """Fetch + parse a feed (convenience; landing uses the raw bytes)."""
        return json.loads(self.fetch_feed_raw(name))


def land_gbfs_snapshot(
    client: GbfsClient,
    storage: Storage,
    feed_name: str,
    system_id: str,
    *,
    epoch: int | None = None,
) -> str:
    """Fetch one feed snapshot and land it, partitioned by day. Returns the object URI."""
    raw = client.fetch_feed_raw(feed_name)
    ts = int(epoch) if epoch is not None else int(datetime.now(UTC).timestamp())
    day = datetime.fromtimestamp(ts, tz=UTC).strftime("%Y-%m-%d")
    key = f"bronze/gbfs/{system_id}/{feed_name}/dt={day}/{feed_name}_{ts}.json"
    return storage.put_bytes(key, raw, content_type="application/json")
