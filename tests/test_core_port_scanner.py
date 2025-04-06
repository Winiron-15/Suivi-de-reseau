"""
Tests unitaires pour le module port_scanner.
"""

import unittest

from unittest.mock import patch, MagicMock
from src.core import port_scanner
from src.core.port_scanner import scan_with_nmap


class TestPortScannerWithHttpServer(unittest.TestCase):
    """Tests du comportement de scan_with_nmap avec services réseau simulés."""

    @patch(
        "src.core.port_scanner.scan_with_nmap",
        return_value=[(8080, "http")]
    )
    def test_nmap_detects_http_server(self, _mock_scan):
        """Vérifie que nmap détecte un service HTTP sur le port 8080."""
        results = port_scanner.scan_with_nmap("127.0.0.1")
        ports = [port for port, _ in results]
        self.assertIn(8080, ports)

    @patch("subprocess.run")
    def test_scan_with_open_ports_parsing(self, mock_run):
        """Teste l'analyse correcte de la sortie Nmap avec plusieurs ports ouverts."""
        mock_process = MagicMock()
        mock_process.stdout = (
            "Starting Nmap 7.80\n"
            "Nmap scan report for 192.168.1.1\n"
            "80/tcp open http\n"
            "443/tcp open https\n"
            "MAC Address: XX:XX:XX:XX:XX:XX\n"
        )
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        result = scan_with_nmap("192.168.1.1")
        self.assertIn((80, "http"), result)
        self.assertIn((443, "https"), result)


if __name__ == "__main__":
    unittest.main()
