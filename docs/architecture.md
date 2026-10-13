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
- `ranking`: score and sort findings into an investigation queue.
- `reports`: format output for CLI, JSON, or dashboard use.
- `models`: shared typed data structures.
- `utils`: logging, file loading, and small shared helpers.

## First MVP Boundary

The first MVP supports CycloneDX JSON for npm packages and OSV enrichment. Reachability, dashboard UI, CI gates, and ML models are later milestones.
