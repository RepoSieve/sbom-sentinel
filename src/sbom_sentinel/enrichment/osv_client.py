"""OSV API client for package/version/ecosystem queries."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OSV_QUERY_URL = "https://api.osv.dev/v1/query"
DEFAULT_TIMEOUT_SECONDS = 20
MAX_RETRIES = 3


class OsvClientError(RuntimeError):
    """Raised when the OSV API cannot be reached or returns an error."""


class OsvClient:
    """Minimal OSV query client using the standard library."""

    def __init__(
        self,
        base_url: str = OSV_QUERY_URL,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds

    def query(
        self,
        package_name: str,
        version: str,
        ecosystem: str,
    ) -> dict[str, Any]:
        body = json.dumps(
            {
                "package": {"name": package_name, "ecosystem": ecosystem},
                "version": version,
            }
        ).encode("utf-8")
        last_error: Exception | None = None
        for attempt in range(MAX_RETRIES):
            request = Request(
                self.base_url,
                data=body,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method="POST",
            )
            try:
                with urlopen(request, timeout=self.timeout_seconds) as response:
                    raw = response.read().decode("utf-8")
                payload = json.loads(raw) if raw.strip() else {}
                if not isinstance(payload, dict):
                    raise OsvClientError("OSV response was not a JSON object.")
                return payload
            except HTTPError as exc:
                last_error = exc
                if exc.code == 429 and attempt < MAX_RETRIES - 1:
                    time.sleep(2**attempt)
                    continue
                raise OsvClientError(f"OSV HTTP error {exc.code}: {exc.reason}") from exc
            except (URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
                last_error = exc
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2**attempt)
                    continue
                raise OsvClientError(f"OSV request failed: {exc}") from exc
        raise OsvClientError(f"OSV request failed: {last_error}")
