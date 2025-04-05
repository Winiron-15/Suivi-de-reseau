import unittest
from src.utils import parsing

class TestParsing(unittest.TestCase):

    def test_extract_latency_linux_format(self):
        output = "rtt min/avg/max/mdev = 0.033/0.045/0.056/0.011 ms"
        self.assertEqual(parsing.extract_latency(output), 0)

    def test_extract_latency_windows_fr_format(self):
        output = "    Moyenne = 123 ms"
        self.assertEqual(parsing.extract_latency(output), 123)

    def test_extract_latency_windows_en_format(self):
        output = "    Average = 85ms"
        self.assertEqual(parsing.extract_latency(output), 85)

    def test_extract_latency_empty(self):
        output = ""
        self.assertIsNone(parsing.extract_latency(output))

    def test_extract_latency_non_matching(self):
        output = "some random text without latency"
        self.assertIsNone(parsing.extract_latency(output))

    def test_resolve_hostname_when_different(self):
        # Simule un vrai resolve en local avec une IP publique connue
        result = parsing.resolve_hostname_if_needed("1.1.1.1", "1.1.1.1")
        self.assertTrue(isinstance(result, str))

    def test_resolve_hostname_when_already_named(self):
        result = parsing.resolve_hostname_if_needed("example.com", "93.184.216.34")
        self.assertEqual(result, "example.com")

if __name__ == "__main__":
    unittest.main()