# Architecture

SBOM Sentinel converts an SBOM into an explainable investigation queue for dependency vulnerabilities.

## MVP Flow

```text
CycloneDX SBOM
    |
    v
SBOM ingestion and normalization
    |
    v
OSV vulnerability enrichment
    |
    v
Baseline risk ranking
    |
    v
Explainable report
```

## Modules

- `ingestion`: parse CycloneDX or SPDX inputs into internal records.
- `enrichment`: add vulnerability evidence from OSV and later sources.
  - `osv_client` posts package/name/version queries to `https://api.osv.dev/v1/query`.
  - `cache` stores raw OSV JSON under `data/cache/osv` keyed by ecosystem, name, and version.
  - `enricher` maps parser records to the enriched finding contract, including `found`, `not_found`, `unknown`, `api_error`, and `unsupported_ecosystem`.
- `ranking`: score and sort findings into an investigation queue.
- `reports`: format output for CLI, JSON, or dashboard use.
- `models`: shared typed data structures.
- `utils`: logging, file loading, and small shared helpers.

## First MVP Boundary

The first MVP supports CycloneDX JSON for npm packages and OSV enrichment. Reachability, dashboard UI, CI gates, and ML models are later milestones.
