import unittest


class ImportTests(unittest.TestCase):
    def test_package_imports(self):
        import sbom_sentinel

        self.assertTrue(sbom_sentinel.__version__)


if __name__ == "__main__":
    unittest.main()
