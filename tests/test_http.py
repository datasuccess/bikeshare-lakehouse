# ── tests/test_http.py ───────────────────────────────────
# Purpose : the resilience contract — retry 429/5xx with backoff, surface 4xx immediately.
# Why     : this is the "real API" reliability story; prove it without hitting the network.
from __future__ import annotations

import httpx
import pytest
import respx
from ingestion import _http


def test_retries_then_succeeds():
    with respx.mock:
        route = respx.get("https://api.test/x").mock(
            side_effect=[httpx.Response(500), httpx.Response(200, json={"ok": True})]
        )
        with httpx.Client() as client:
            resp = _http.get(client, "https://api.test/x", backoff=0)
        assert resp.json() == {"ok": True}
        assert route.call_count == 2


def test_gives_up_on_persistent_5xx():
    with respx.mock:
        respx.get("https://api.test/x").mock(return_value=httpx.Response(503))
        with httpx.Client() as client, pytest.raises(_http.RetryableHTTPError):
            _http.get(client, "https://api.test/x", max_attempts=3, backoff=0)


def test_does_not_retry_4xx():
    with respx.mock:
        route = respx.get("https://api.test/x").mock(return_value=httpx.Response(404))
        with httpx.Client() as client, pytest.raises(httpx.HTTPStatusError):
            _http.get(client, "https://api.test/x", backoff=0)
        assert route.call_count == 1
