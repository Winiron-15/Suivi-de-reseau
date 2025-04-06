# Tests pour le module 'core/scanner_threaded'



# -------- test_scanner_threaded.py --------
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

# -------- test_coverage_extensions.py --------
from unittest.mock import patch, mock_open
import subprocess
import socket
import builtins

import src.utils.csv_utils
import src.utils.parsing
import src.core.port_scanner
import src.core.scanner_threaded

class TestCoverageExtensions(unittest.TestCase):

    def test_csv_utils_save_to_csv(self):
        results = [("host1", "192.168.1.1", "Active", 10)]
        m = mock_open()
        with patch.object(builtins, "open", m):
            src.utils.csv_utils.save_to_csv(results, "test_output.csv")
            m.assert_called_once()

    def test_parsing_latency_fallback(self):
        output = "temps=42 ms"
        latency = src.utils.parsing.extract_latency(output)
        self.assertEqual(latency, 42)

    def test_parsing_resolve_hostname_exception(self):
        with patch("socket.gethostbyaddr", side_effect=socket.herror):
            result = src.utils.parsing.resolve_hostname_if_needed("192.168.1.1", "192.168.1.1")
            self.assertEqual(result, "192.168.1.1")

    def test_port_scanner_timeout(self):
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("nmap", 60)):
            result = src.core.port_scanner.scan_with_nmap("192.168.1.1")
            self.assertEqual(result, [])

    def test_port_scanner_called_process_error(self):
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "nmap")):
            result = src.core.port_scanner.scan_with_nmap("192.168.1.1")
            self.assertEqual(result, [])

    def test_port_scanner_os_error(self):
        with patch("subprocess.run", side_effect=OSError("nmap error")):
            result = src.core.port_scanner.scan_with_nmap("192.168.1.1")
            self.assertEqual(result, [])

    def test_scanner_threaded_exception(self):
        with patch("src.core.scanner_threaded.subprocess.run", side_effect=Exception("ping failed")):
            result = src.core.scanner_threaded.ping_ip("host", "192.168.1.1")
            self.assertEqual(result[2], "Error: ping failed")
            self.assertIsNone(result[3])

if __name__ == "__main__":
    unittest.main()