# Demo Plan

The Friday demo should prove a working vertical slice.

## Target Command

```bash
python -m sbom_sentinel --help
```

Later, this should become:

```bash
python -m sbom_sentinel demo data/samples/cyclonedx-npm-sample.json
```

## Demo Steps

1. Show the repo structure.
2. Show the sample SBOM.
3. Run the parser.
4. Run OSV enrichment.
5. Run baseline ranking.
6. Explain the top ranked finding.
7. Show tests and known limitations.

## Friday Success Criteria

The team can explain how an SBOM becomes an explainable investigation queue.
