# OSV Enrichment And Evidence Cache

This note explains how SBOM Sentinel turns parser output into ranking-ready findings.

## Command

```bash
PYTHONPATH=src python3 -m sbom_sentinel enrich \
  --input tests/fixtures/sample_packages.json \
  --output data/outputs/enriched.json \
  --cache-dir data/cache/osv
```

Repeat the same command with `--offline` to use only cached OSV responses.

## Request

Each parsed package is mapped to an [OSV query](https://google.github.io/osv.dev/):

```json
{
  "package": {
    "name": "lodash",
    "ecosystem": "npm"
  },
  "version": "4.17.20"
}
```

Ecosystem mapping currently supports npm first, plus aliases for PyPI, Maven, Go, crates.io, RubyGems, NuGet, Packagist, and Hex. Unknown ecosystems are not queried.

## Response handling

OSV returns either `{"vulns": [...]}` or an empty object when nothing is found.

For each vulnerability we keep:

- `vulnerability_id` (`id`)
- `aliases`
- `summary`
- `severity` (GitHub `database_specific.severity`, otherwise a CVSS v3 band)
- compact `affected_evidence` for the matching package
- `source_metadata` (`published`, `modified`, mapped OSV ecosystem)

A package with several OSV records produces several findings.

## Evidence status

Missing evidence is never treated as safe.

| Status | Meaning |
| --- | --- |
| `found` | OSV returned at least one vulnerability. |
| `not_found` | OSV returned no records for that name/version. This is not a safety proof. |
| `unknown` | Package name or version is missing, or the response could not be read. |
| `api_error` | Network/HTTP failure, or cache miss while `--offline`. |
| `unsupported_ecosystem` | The parser ecosystem is not mapped to OSV yet. |

## Cache behavior

Cache files live under `--cache-dir` (default `data/cache/osv`).

The cache key is `ecosystem + package name + version`. The first live lookup writes the raw OSV JSON. Later runs reuse that file and set `cache_hit: true`, so demos do not depend on the network after the first successful query.

Corrupt cache files are ignored and the client is called again. Cache write failures do not drop a successful OSV result.

## Sample output

See `data/samples/enriched-findings.json` for a checked-in example produced from `tests/fixtures/sample_packages.json` with the live OSV API mocked in tests.
