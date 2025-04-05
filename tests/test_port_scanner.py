import unittest
from unittest.mock import patch
from src.core import port_scanner

class TestPortScanner(unittest.TestCase):
    @patch("subprocess.run")
    def test_scan_with_nmap(self, mock_run):
        mock_run.return_value.stdout = "22/tcp open ssh\n80/tcp open http"
        mock_run.return_value.returncode = 0
        result = port_scanner.scan_with_nmap("192.168.1.1")
        self.assertIn((22, "ssh"), result)
        self.assertIn((80, "http"), result)