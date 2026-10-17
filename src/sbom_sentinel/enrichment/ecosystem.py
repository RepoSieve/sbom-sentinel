"""Map parser ecosystem values to OSV ecosystem identifiers."""

from __future__ import annotations

OSV_ECOSYSTEMS = {
    "npm": "npm",
    "pypi": "PyPI",
    "python": "PyPI",
    "maven": "Maven",
    "go": "Go",
    "golang": "Go",
    "crates.io": "crates.io",
    "cargo": "crates.io",
    "rubygems": "RubyGems",
    "nuget": "NuGet",
    "packagist": "Packagist",
    "hex": "Hex",
}


def map_osv_ecosystem(value: str | None) -> str | None:
    """Return the OSV ecosystem name, or None if unsupported/missing."""
    if not value or not str(value).strip():
        return None
    key = str(value).strip()
    mapped = OSV_ECOSYSTEMS.get(key)
    if mapped:
        return mapped
    mapped = OSV_ECOSYSTEMS.get(key.lower())
    return mapped
