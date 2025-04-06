"""
Tests unitaires pour scanner_threaded et couverture associée.
"""

import subprocess
import socket
import builtins
import unittest

from unittest.mock import patch, mock_open
from src.core import scanner_threaded
import src.utils.csv_utils
import src.utils.parsing
import src.core.port_scanner


class TestScannerThreaded(unittest.TestCase):
    """Tests des fonctions principales de scanner_threaded."""

    @patch("src.core.scanner_threaded.subprocess.run")
    @patch("src.core.scanner_threaded.extract_latency", return_value=12)
    @patch(
        "src.core.scanner_threaded.build_ping_command",
        return_value=["ping", "-c", "1", "127.0.0.1"]
    )
    def test_scan_ips_success(
        self,
        _mock_build,
        _mock_extract,
        mock_run
    ):
        """Doit renvoyer un hôte actif avec latence correcte"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "ping output"

        machines = [("localhost", "127.0.0.1")]
        results = scanner_threaded.scan_ips(machines, threads=1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "localhost")
        self.assertEqual(results[0][2], "Active")
        self.assertEqual(results[0][3], 12)

    @patch("src.core.scanner_threaded.subprocess.run")
    @patch(
        "src.core.scanner_threaded.build_ping_command",
        return_value=["ping", "-c", "1", "256.256.256.256"]
    )
    def test_scan_ips_failure(self, _mock_build, mock_run):
        """Doit renvoyer un hôte inactif et latence None"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""

        machines = [("badhost", "256.256.256.256")]
        results = scanner_threaded.scan_ips(machines, threads=1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "badhost")
        self.assertEqual(results[0][2], "Inactive")
        self.assertIsNone(results[0][3])


class TestCoverageExtensions(unittest.TestCase):
    """Tests de couverture additionnelle pour utils et port_scanner."""

    def test_csv_utils_save_to_csv(self):
        """Teste que le CSV est bien sauvegardé avec mock open"""
        results = [("host1", "192.168.1.1", "Active", 10)]
        m = mock_open()
        with patch.object(builtins, "open", m):
            src.utils.csv_utils.save_to_csv(results, "test_output.csv")
            m.assert_called_once()

    def test_parsing_latency_fallback(self):
        """Teste l'extraction de latence alternative (fallback)"""
        output = "temps=42 ms"
        latency = src.utils.parsing.extract_latency(output)
        self.assertEqual(latency, 42)

    def test_parsing_resolve_hostname_exception(self):
        """Teste qu'un échec de résolution DNS retourne l'IP"""
        with patch("socket.gethostbyaddr", side_effect=socket.herror):
            result = src.utils.parsing.resolve_hostname_if_needed(
                "192.168.1.1", "192.168.1.1"
            )
            self.assertEqual(result, "192.168.1.1")

    def test_port_scanner_timeout(self):
        """Doit retourner [] en cas de timeout de nmap"""
        with patch(
            "subprocess.run",
            side_effect=subprocess.TimeoutExpired("nmap", 60)
        ):
            result = src.core.port_scanner.scan_with_nmap("192.168.1.1")
            self.assertEqual(result, [])

    def test_port_scanner_called_process_error(self):
        """Doit retourner [] si nmap plante (CalledProcessError)"""
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "nmap")
        ):
            result = src.core.port_scanner.scan_with_nmap("192.168.1.1")
            self.assertEqual(result, [])

    def test_port_scanner_os_error(self):
        """Doit retourner [] en cas d'OSError (nmap absent)"""
        with patch(
            "subprocess.run",
            side_effect=OSError("nmap error")
        ):
            result = src.core.port_scanner.scan_with_nmap("192.168.1.1")
            self.assertEqual(result, [])

    def test_scanner_threaded_exception(self):
        """Doit retourner une erreur lisible si le ping échoue totalement"""
        with patch(
            "src.core.scanner_threaded.subprocess.run",
            side_effect=Exception("ping failed")
        ):
            result = src.core.scanner_threaded.ping_ip("host", "192.168.1.1")
            self.assertEqual(result[2], "Error: ping failed")
            self.assertIsNone(result[3])


if __name__ == "__main__":
    unittest.main()
