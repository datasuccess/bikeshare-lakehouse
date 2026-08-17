# ── tests/test_gbfs_client.py ────────────────────────────
# Purpose : GBFS discovery is cached, snapshots land at a day-partitioned key, unknown feeds raise.
from __future__ import annotations

import httpx
import pytest
import respx
from ingestion.gbfs_client import GbfsClient, land_gbfs_snapshot


def test_discover_caches_and_lists_feeds(gbfs_discovery):
    with respx.mock:
        disco = respx.get("https://gbfs.test/gbfs.json").mock(
            return_value=httpx.Response(200, json=gbfs_discovery)
        )
        client = GbfsClient("https://gbfs.test/gbfs.json", backoff=0)
        feeds = client.discover()
        client.discover()  # second call should use the cache

        assert set(feeds) == {"station_information", "station_status"}
        assert disco.call_count == 1


def test_land_snapshot_writes_partitioned_key(storage, gbfs_discovery):
    with respx.mock:
        respx.get("https://gbfs.test/gbfs.json").mock(
            return_value=httpx.Response(200, json=gbfs_discovery)
        )
        respx.get("https://feeds.test/station_status.json").mock(
            return_value=httpx.Response(200, json={"data": {"stations": []}})
        )
        client = GbfsClient("https://gbfs.test/gbfs.json", backoff=0)
        uri = land_gbfs_snapshot(client, storage, "station_status", "dca-cabi", epoch=1704067200)

        assert uri == (
            "mem://bronze/gbfs/dca-cabi/station_status/dt=2024-01-01/station_status_1704067200.json"
        )
        assert len(storage.objects) == 1


def test_unknown_feed_raises(gbfs_discovery):
    with respx.mock:
        respx.get("https://gbfs.test/gbfs.json").mock(
            return_value=httpx.Response(200, json=gbfs_discovery)
        )
        client = GbfsClient("https://gbfs.test/gbfs.json", backoff=0)
        with pytest.raises(KeyError):
            client.fetch_feed_raw("nonexistent")
