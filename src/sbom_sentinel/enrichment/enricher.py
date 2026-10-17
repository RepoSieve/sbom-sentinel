"""Turn normalized packages into ranking-ready OSV findings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sbom_sentinel.enrichment.cache import EvidenceCache
from sbom_sentinel.enrichment.ecosystem import map_osv_ecosystem
from sbom_sentinel.enrichment.osv_client import OsvClient, OsvClientError
from sbom_sentinel.models.vulnerability import (
    EVIDENCE_API_ERROR,
    EVIDENCE_FOUND,
    EVIDENCE_NOT_FOUND,
    EVIDENCE_UNKNOWN,
    EVIDENCE_UNSUPPORTED,
    EnrichedFinding,
)

SEVERITY_ALIASES = {
    "CRITICAL": "CRITICAL",
    "HIGH": "HIGH",
    "MEDIUM": "MEDIUM",
    "MODERATE": "MEDIUM",
    "LOW": "LOW",
    "UNKNOWN": "UNKNOWN",
}


def load_packages(path: str | Path) -> list[dict[str, Any]]:
    """Load parser-shaped package records from JSON."""
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        packages = payload.get("packages", payload.get("normalized_packages"))
        if isinstance(packages, list):
            return packages
    raise ValueError("Package input must be a JSON list or an object with a packages array.")


def write_findings(path: str | Path, findings: list[EnrichedFinding]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    records = [finding.to_dict() for finding in findings]
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2)
        handle.write("\n")


def enrich_packages(
    packages: list[dict[str, Any]],
    *,
    cache: EvidenceCache,
    client: OsvClient | None = None,
    offline: bool = False,
) -> list[EnrichedFinding]:
    """Enrich normalized packages. Missing evidence is marked unknown, never safe."""
    osv_client = client or OsvClient()
    findings: list[EnrichedFinding] = []
    for package in packages:
        findings.extend(_enrich_one(package, cache=cache, client=osv_client, offline=offline))
    return findings


def _enrich_one(
    package: dict[str, Any],
    *,
    cache: EvidenceCache,
    client: OsvClient,
    offline: bool,
) -> list[EnrichedFinding]:
    name = str(package.get("package_name") or "").strip()
    version = str(package.get("version") or "").strip()
    raw_ecosystem = package.get("ecosystem")
    ecosystem = str(raw_ecosystem).strip() if raw_ecosystem else ""
    common = {
        "package_name": name or "unknown",
        "version": version or "unknown",
        "ecosystem": ecosystem or "unknown",
        "purl": package.get("purl"),
        "bom_ref": package.get("bom_ref"),
    }

    if not name or not version:
        return [
            EnrichedFinding(
                **common,
                vulnerability_id=None,
                summary="Package name or version is missing; vulnerability evidence is unknown.",
                evidence_status=EVIDENCE_UNKNOWN,
                source_metadata={"reason": "missing_package_or_version"},
            )
        ]

    osv_ecosystem = map_osv_ecosystem(ecosystem)
    if osv_ecosystem is None:
        return [
            EnrichedFinding(
                **common,
                vulnerability_id=None,
                summary=f"Ecosystem {ecosystem!r} is not supported by the OSV client yet.",
                evidence_status=EVIDENCE_UNSUPPORTED,
                source_metadata={"reason": "unsupported_ecosystem"},
            )
        ]

    cached = cache.get(osv_ecosystem, name, version)
    cache_hit = cached is not None
    payload: dict[str, Any]
    if cached is not None:
        payload = cached
    elif offline:
        return [
            EnrichedFinding(
                **common,
                vulnerability_id=None,
                summary="No cached OSV evidence and live API access is disabled.",
                evidence_status=EVIDENCE_API_ERROR,
                source_metadata={"reason": "offline_cache_miss"},
            )
        ]
    else:
        try:
            payload = client.query(name, version, osv_ecosystem)
        except OsvClientError as exc:
            return [
                EnrichedFinding(
                    **common,
                    vulnerability_id=None,
                    summary=str(exc),
                    evidence_status=EVIDENCE_API_ERROR,
                    source_metadata={"reason": "osv_request_failed"},
                )
            ]
        try:
            cache.set(osv_ecosystem, name, version, payload)
        except OSError:
            # Cache failure must not hide the OSV result.
            pass

    vulns = payload.get("vulns") or []
    if not vulns:
        return [
            EnrichedFinding(
                **common,
                vulnerability_id=None,
                summary="OSV returned no vulnerabilities for this package version.",
                evidence_status=EVIDENCE_NOT_FOUND,
                cache_hit=cache_hit,
                source_metadata={"osv_ecosystem": osv_ecosystem, "vuln_count": 0},
            )
        ]

    findings = []
    for vuln in vulns:
        if not isinstance(vuln, dict):
            continue
        findings.append(
            EnrichedFinding(
                **common,
                vulnerability_id=str(vuln.get("id") or "UNKNOWN"),
                aliases=_as_str_list(vuln.get("aliases")),
                summary=str(vuln.get("summary") or vuln.get("details") or "OSV vulnerability record."),
                severity=_severity_from_osv(vuln),
                evidence_status=EVIDENCE_FOUND,
                cache_hit=cache_hit,
                affected_evidence=_affected_evidence(vuln, name, osv_ecosystem),
                source_metadata={
                    "osv_ecosystem": osv_ecosystem,
                    "published": vuln.get("published"),
                    "modified": vuln.get("modified"),
                    "schema_version": vuln.get("schema_version"),
                },
            )
        )
    if not findings:
        return [
            EnrichedFinding(
                **common,
                vulnerability_id=None,
                summary="OSV response contained unreadable vulnerability records.",
                evidence_status=EVIDENCE_UNKNOWN,
                cache_hit=cache_hit,
                source_metadata={"reason": "unreadable_vuln_records"},
            )
        ]
    return findings


def _as_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _severity_from_osv(vuln: dict[str, Any]) -> str:
    database = vuln.get("database_specific") or {}
    db_severity = database.get("severity") if isinstance(database, dict) else None
    if isinstance(db_severity, str) and db_severity.strip():
        return SEVERITY_ALIASES.get(db_severity.strip().upper(), db_severity.strip().upper())
    records = vuln.get("severity") or []
    if isinstance(records, list):
        for record in records:
            if not isinstance(record, dict):
                continue
            score = str(record.get("score") or "")
            if score.startswith("CVSS:3"):
                mapped = _cvss3_band(score)
                if mapped:
                    return mapped
            label = record.get("type")
            if isinstance(label, str) and label.upper() in SEVERITY_ALIASES:
                return SEVERITY_ALIASES[label.upper()]
    return "UNKNOWN"


def _cvss3_band(vector: str) -> str | None:
    """Band from impact metrics when a numeric base score is not provided."""
    metrics = dict(part.split(":", 1) for part in vector.split("/") if ":" in part)
    confidentiality = metrics.get("C", "N")
    integrity = metrics.get("I", "N")
    availability = metrics.get("A", "N")
    impacts = {confidentiality, integrity, availability}
    if "H" in impacts and metrics.get("PR") in {"N", "L"}:
        return "HIGH"
    if "H" in impacts:
        return "HIGH"
    if "L" in impacts:
        return "MEDIUM"
    return "LOW"


def _affected_evidence(vuln: dict[str, Any], package_name: str, ecosystem: str) -> dict[str, Any]:
    affected = vuln.get("affected") or []
    if not isinstance(affected, list):
        return {"package_name": package_name, "ecosystem": ecosystem}
    matched = None
    for item in affected:
        if not isinstance(item, dict):
            continue
        pkg = item.get("package") or {}
        if isinstance(pkg, dict) and str(pkg.get("name")) == package_name:
            matched = item
            break
    if matched is None and affected:
        first = affected[0]
        matched = first if isinstance(first, dict) else None
    if not matched:
        return {"package_name": package_name, "ecosystem": ecosystem}
    package = matched.get("package") if isinstance(matched.get("package"), dict) else {}
    ranges = matched.get("ranges") if isinstance(matched.get("ranges"), list) else []
    compact_ranges = []
    for item in ranges[:3]:
        if isinstance(item, dict):
            compact_ranges.append({"type": item.get("type"), "events": item.get("events")})
    return {
        "package_name": package.get("name", package_name),
        "ecosystem": package.get("ecosystem", ecosystem),
        "purl": package.get("purl"),
        "ranges": compact_ranges,
    }
