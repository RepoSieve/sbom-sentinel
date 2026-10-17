import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sbom_sentinel.enrichment.cache import EvidenceCache
from sbom_sentinel.enrichment.ecosystem import map_osv_ecosystem
from sbom_sentinel.enrichment.enricher import enrich_packages, load_packages
from sbom_sentinel.enrichment.osv_client import OsvClientError
from sbom_sentinel.models.vulnerability import (
    EVIDENCE_API_ERROR,
    EVIDENCE_FOUND,
    EVIDENCE_NOT_FOUND,
    EVIDENCE_UNKNOWN,
    EVIDENCE_UNSUPPORTED,
)


FIXTURE_PACKAGES = Path(__file__).parent / "fixtures" / "sample_packages.json"

FOUND_RESPONSE = {
    "vulns": [
        {
            "id": "GHSA-35jh-r3h4-6jhm",
            "aliases": ["CVE-2021-23337"],
            "summary": "Command Injection in lodash",
            "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H"}],
            "database_specific": {"severity": "HIGH"},
            "affected": [
                {
                    "package": {"name": "lodash", "ecosystem": "npm", "purl": "pkg:npm/lodash"},
                    "ranges": [{"type": "SEMVER", "events": [{"introduced": "0"}, {"fixed": "4.17.21"}]}],
                }
            ],
            "published": "2021-02-15T00:00:00Z",
            "modified": "2021-02-15T00:00:00Z",
        }
    ]
}


class EnrichmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.cache = EvidenceCache(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_found_vulnerability(self) -> None:
        packages = [
            {
                "package_name": "lodash",
                "version": "4.17.20",
                "ecosystem": "npm",
                "purl": "pkg:npm/lodash@4.17.20",
            }
        ]
        with patch(
            "sbom_sentinel.enrichment.enricher.OsvClient.query",
            return_value=FOUND_RESPONSE,
        ) as query:
            findings = enrich_packages(packages, cache=self.cache)

        self.assertEqual(query.call_count, 1)
        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding.evidence_status, EVIDENCE_FOUND)
        self.assertEqual(finding.vulnerability_id, "GHSA-35jh-r3h4-6jhm")
        self.assertEqual(finding.aliases, ["CVE-2021-23337"])
        self.assertEqual(finding.severity, "HIGH")
        self.assertEqual(finding.affected_evidence["package_name"], "lodash")
        self.assertFalse(finding.cache_hit)
        self.assertTrue(self.cache.path_for("npm", "lodash", "4.17.20").is_file())

    def test_no_vulnerability_found(self) -> None:
        packages = [{"package_name": "left-pad", "version": "1.3.0", "ecosystem": "npm"}]
        with patch("sbom_sentinel.enrichment.enricher.OsvClient.query", return_value={}):
            findings = enrich_packages(packages, cache=self.cache)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].evidence_status, EVIDENCE_NOT_FOUND)
        self.assertIsNone(findings[0].vulnerability_id)
        self.assertNotEqual(findings[0].evidence_status, "safe")

    def test_missing_fields_are_unknown_not_safe(self) -> None:
        packages = [{"package_name": "incomplete-lib", "version": "", "ecosystem": "npm"}]
        with patch("sbom_sentinel.enrichment.enricher.OsvClient.query") as query:
            findings = enrich_packages(packages, cache=self.cache)

        query.assert_not_called()
        self.assertEqual(findings[0].evidence_status, EVIDENCE_UNKNOWN)
        self.assertIn("missing", findings[0].summary.lower())

    def test_unsupported_ecosystem(self) -> None:
        packages = [{"package_name": "internal-tool", "version": "1.0.0", "ecosystem": "internal"}]
        with patch("sbom_sentinel.enrichment.enricher.OsvClient.query") as query:
            findings = enrich_packages(packages, cache=self.cache)

        query.assert_not_called()
        self.assertEqual(findings[0].evidence_status, EVIDENCE_UNSUPPORTED)

    def test_api_error(self) -> None:
        packages = [{"package_name": "lodash", "version": "4.17.20", "ecosystem": "npm"}]
        with patch(
            "sbom_sentinel.enrichment.enricher.OsvClient.query",
            side_effect=OsvClientError("OSV request failed: timeout"),
        ):
            findings = enrich_packages(packages, cache=self.cache)

        self.assertEqual(findings[0].evidence_status, EVIDENCE_API_ERROR)
        self.assertIn("timeout", findings[0].summary)

    def test_cache_hit_skips_network(self) -> None:
        packages = [{"package_name": "lodash", "version": "4.17.20", "ecosystem": "npm"}]
        self.cache.set("npm", "lodash", "4.17.20", FOUND_RESPONSE)
        with patch("sbom_sentinel.enrichment.enricher.OsvClient.query") as query:
            findings = enrich_packages(packages, cache=self.cache)

        query.assert_not_called()
        self.assertTrue(findings[0].cache_hit)
        self.assertEqual(findings[0].evidence_status, EVIDENCE_FOUND)

    def test_offline_cache_miss_is_api_error(self) -> None:
        packages = [{"package_name": "lodash", "version": "4.17.20", "ecosystem": "npm"}]
        with patch("sbom_sentinel.enrichment.enricher.OsvClient.query") as query:
            findings = enrich_packages(packages, cache=self.cache, offline=True)

        query.assert_not_called()
        self.assertEqual(findings[0].evidence_status, EVIDENCE_API_ERROR)

    def test_corrupt_cache_falls_back_to_client(self) -> None:
        packages = [{"package_name": "lodash", "version": "4.17.20", "ecosystem": "npm"}]
        path = self.cache.path_for("npm", "lodash", "4.17.20")
        path.write_text("{not-json", encoding="utf-8")
        with patch(
            "sbom_sentinel.enrichment.enricher.OsvClient.query",
            return_value=FOUND_RESPONSE,
        ) as query:
            findings = enrich_packages(packages, cache=self.cache)

        self.assertEqual(query.call_count, 1)
        self.assertEqual(findings[0].evidence_status, EVIDENCE_FOUND)

    def test_load_sample_packages_fixture(self) -> None:
        packages = load_packages(FIXTURE_PACKAGES)
        self.assertEqual(len(packages), 4)
        self.assertEqual(packages[0]["package_name"], "lodash")

    def test_ecosystem_mapping(self) -> None:
        self.assertEqual(map_osv_ecosystem("npm"), "npm")
        self.assertEqual(map_osv_ecosystem("PyPI"), "PyPI")
        self.assertEqual(map_osv_ecosystem("python"), "PyPI")
        self.assertIsNone(map_osv_ecosystem("internal"))


class CliEnrichTests(unittest.TestCase):
    def test_enrich_command(self) -> None:
        from sbom_sentinel.cli import main

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "enriched.json"
            cache_dir = Path(tmp) / "cache"
            def fake_query(name: str, version: str, ecosystem: str):
                if name == "lodash":
                    return FOUND_RESPONSE
                return {}

            with patch(
                "sbom_sentinel.enrichment.enricher.OsvClient.query",
                side_effect=fake_query,
            ):
                code = main(
                    [
                        "enrich",
                        "--input",
                        str(FIXTURE_PACKAGES),
                        "--output",
                        str(output),
                        "--cache-dir",
                        str(cache_dir),
                    ]
                )
            self.assertEqual(code, 0)
            findings = json.loads(output.read_text(encoding="utf-8"))
            statuses = {item["evidence_status"] for item in findings}
            self.assertIn(EVIDENCE_FOUND, statuses)
            self.assertIn(EVIDENCE_NOT_FOUND, statuses)
            self.assertIn(EVIDENCE_UNKNOWN, statuses)
            self.assertIn(EVIDENCE_UNSUPPORTED, statuses)


if __name__ == "__main__":
    unittest.main()
