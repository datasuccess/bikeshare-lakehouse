# ── ingestion/_http.py ───────────────────────────────────
# Purpose : one resilient HTTP GET used by every loader.
# Why     : real feeds 429/5xx sometimes; retry those with backoff, never 4xx (ADR-009).
# Inputs  : an httpx.Client + url    Outputs: an httpx.Response (raises after N attempts)
# Docs    : ingestion/LEARNING.md  (see "why retry only 429/5xx")
from __future__ import annotations

import httpx
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


class RetryableHTTPError(Exception):
    """Raised for HTTP 429 / 5xx so tenacity retries them. 4xx are surfaced immediately."""


def get(
    client: httpx.Client,
    url: str,
    *,
    max_attempts: int = 5,
    backoff: float = 1.0,
    backoff_max: float = 30.0,
) -> httpx.Response:
    """GET ``url`` with exponential backoff on transient failures (transport errors, 429, 5xx)."""
    retryer = Retrying(
        reraise=True,
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=backoff, max=backoff_max),
        retry=retry_if_exception_type((httpx.TransportError, RetryableHTTPError)),
    )
    return retryer(_get_once, client, url)


def _get_once(client: httpx.Client, url: str) -> httpx.Response:
    resp = client.get(url)
    if resp.status_code == 429 or resp.status_code >= 500:
        raise RetryableHTTPError(f"HTTP {resp.status_code} for {url}")
    resp.raise_for_status()  # other 4xx -> HTTPStatusError, not retried
    return resp
