"""Command-line entry point for SBOM Sentinel."""

from __future__ import annotations

import argparse
from pathlib import Path

from sbom_sentinel.enrichment.cache import EvidenceCache
from sbom_sentinel.enrichment.enricher import enrich_packages, load_packages, write_findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sbom_sentinel",
        description="Explainable SBOM vulnerability triage prototype.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show the package version.",
    )
    subparsers = parser.add_subparsers(dest="command")

    enrich = subparsers.add_parser(
        "enrich",
        help="Query OSV for normalized packages and write enriched findings JSON.",
    )
    enrich.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to parser-shaped package JSON (list or {\"packages\": [...]}).",
    )
    enrich.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to write enriched findings JSON.",
    )
    enrich.add_argument(
        "--cache-dir",
        default="data/cache/osv",
        help="Local OSV evidence cache directory.",
    )
    enrich.add_argument(
        "--offline",
        action="store_true",
        help="Use the local cache only; do not call the OSV API.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        from . import __version__

        print(__version__)
        return 0
    if args.command == "enrich":
        return _run_enrich(args)
    parser.print_help()
    return 0


def _run_enrich(args: argparse.Namespace) -> int:
    packages = load_packages(args.input)
    cache = EvidenceCache(Path(args.cache_dir))
    findings = enrich_packages(packages, cache=cache, offline=args.offline)
    write_findings(args.output, findings)
    print(f"Wrote {len(findings)} finding(s) to {args.output}")
    return 0
