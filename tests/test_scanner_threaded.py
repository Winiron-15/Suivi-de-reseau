import unittest
from unittest.mock import patch, MagicMock
from src.core import scanner_threaded

class TestScannerThreaded(unittest.TestCase):

    @patch("src.core.scanner_threaded.subprocess.run")
    @patch("src.core.scanner_threaded.extract_latency", return_value=12)
    @patch("src.core.scanner_threaded.build_ping_command", return_value=["ping", "-c", "1", "127.0.0.1"])
    def test_scan_ips_success(self, mock_build, mock_latency, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "ping output"

        machines = [("localhost", "127.0.0.1")]
        results = scanner_threaded.scan_ips(machines, threads=1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "localhost")
        self.assertEqual(results[0][2], "Active")
        self.assertEqual(results[0][3], 12)

    @patch("src.core.scanner_threaded.subprocess.run")
    @patch("src.core.scanner_threaded.build_ping_command", return_value=["ping", "-c", "1", "256.256.256.256"])
    def test_scan_ips_failure(self, mock_build, mock_run):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""

        machines = [("badhost", "256.256.256.256")]
        results = scanner_threaded.scan_ips(machines, threads=1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "badhost")
        self.assertEqual(results[0][2], "Inactive")
        self.assertIsNone(results[0][3])

if __name__ == "__main__":
    unittest.main()