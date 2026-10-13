# Data Contracts

These contracts keep work between team members compatible.

## Normalized Package

```json
{
  "package_name": "example",
  "version": "1.0.0",
  "ecosystem": "npm",
  "purl": "pkg:npm/example@1.0.0",
  "bom_ref": "pkg:npm/example@1.0.0",
  "source_file": "data/samples/cyclonedx-npm-sample.json",
  "evidence_status": "parsed"
}
```

## Normalized Dependency

```json
{
  "parent_ref": "root",
  "child_ref": "pkg:npm/example@1.0.0",
  "dependency_type": "direct",
  "depth": 1
}
```

## Enriched Finding

```json
{
  "package_name": "example",
  "version": "1.0.0",
  "ecosystem": "npm",
  "vulnerability_id": "OSV-EXAMPLE-1",
  "aliases": ["CVE-EXAMPLE-1"],
  "summary": "Example vulnerability summary",
  "severity": "HIGH",
  "evidence_status": "found"
}
```

## Ranked Finding

```json
{
  "rank": 1,
  "package_name": "example",
  "vulnerability_id": "OSV-EXAMPLE-1",
  "score": 87.5,
  "priority": "fix_now",
  "explanation_factors": [
    "high severity",
    "direct dependency",
    "reachability unknown"
  ]
}
```

## Evidence Status Values

- `parsed`
- `found`
- `not_found`
- `unknown`
- `api_error`
- `unsupported_ecosystem`
