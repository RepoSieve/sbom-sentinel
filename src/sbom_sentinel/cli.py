"""Command-line entry point for SBOM Sentinel."""

import argparse


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
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.version:
        from . import __version__

        print(__version__)
    else:
        parser.print_help()
    return 0
