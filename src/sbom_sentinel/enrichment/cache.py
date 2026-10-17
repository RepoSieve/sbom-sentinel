"""Local JSON evidence cache keyed by ecosystem, package name, and version."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


def cache_key(ecosystem: str, package_name: str, version: str) -> str:
    raw = f"{ecosystem.strip().lower()}|{package_name.strip().lower()}|{version.strip()}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{ecosystem}_{package_name}_{version}")
    return f"{safe_name[:80]}_{digest}.json"


class EvidenceCache:
    """Filesystem cache of OSV query responses."""

    def __init__(self, cache_dir: str | Path) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def path_for(self, ecosystem: str, package_name: str, version: str) -> Path:
        return self.cache_dir / cache_key(ecosystem, package_name, version)

    def get(self, ecosystem: str, package_name: str, version: str) -> dict[str, Any] | None:
        path = self.path_for(ecosystem, package_name, version)
        if not path.is_file():
            return None
        try:
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return None
        if not isinstance(payload, dict):
            return None
        return payload

    def set(
        self,
        ecosystem: str,
        package_name: str,
        version: str,
        payload: dict[str, Any],
    ) -> None:
        path = self.path_for(ecosystem, package_name, version)
        tmp = path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        tmp.replace(path)
