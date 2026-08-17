# ── ingestion/storage.py ─────────────────────────────────
# Purpose : read/write raw bytes in the object store (Bronze), behind a small interface.
# Why     : the interface lets the SAME logic target MinIO/S3 in prod and an in-memory double
#           in tests — no network needed to unit-test ingestion/landing (ADR-002).
# Inputs  : keys + bytes           Outputs: URIs / bytes / key lists
# Docs    : docs/01-architecture.md
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Storage(Protocol):
    """Minimal object-store contract used by the loaders (Phase 1) and landing (Phase 2)."""

    def put_bytes(self, key: str, data: bytes, *, content_type: str = ...) -> str: ...

    def exists(self, key: str) -> bool: ...

    def get_bytes(self, key: str) -> bytes: ...

    def list_keys(self, prefix: str) -> list[str]: ...


class InMemoryStorage:
    """A dict-backed store — the test double, and handy for dry runs."""

    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}

    def put_bytes(
        self, key: str, data: bytes, *, content_type: str = "application/octet-stream"
    ) -> str:
        self.objects[key] = data
        return f"mem://{key}"

    def exists(self, key: str) -> bool:
        return key in self.objects

    def get_bytes(self, key: str) -> bytes:
        return self.objects[key]

    def list_keys(self, prefix: str) -> list[str]:
        return sorted(k for k in self.objects if k.startswith(prefix))


class S3Storage:
    """S3-API store — MinIO locally (via endpoint_url) or AWS S3 in the cloud. Same code."""

    def __init__(self, settings) -> None:  # settings: config.Settings
        import boto3  # lazy import so tests don't require boto3

        self._bucket = settings.bucket
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.endpoint_url,
            aws_access_key_id=settings.access_key,
            aws_secret_access_key=settings.secret_key,
            region_name=settings.region,
        )

    def put_bytes(
        self, key: str, data: bytes, *, content_type: str = "application/octet-stream"
    ) -> str:
        self._client.put_object(Bucket=self._bucket, Key=key, Body=data, ContentType=content_type)
        return f"s3://{self._bucket}/{key}"

    def exists(self, key: str) -> bool:
        from botocore.exceptions import ClientError

        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
        except ClientError:
            return False
        return True

    def get_bytes(self, key: str) -> bytes:
        return self._client.get_object(Bucket=self._bucket, Key=key)["Body"].read()

    def list_keys(self, prefix: str) -> list[str]:
        keys: list[str] = []
        paginator = self._client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self._bucket, Prefix=prefix):
            keys.extend(obj["Key"] for obj in page.get("Contents", []))
        return keys
