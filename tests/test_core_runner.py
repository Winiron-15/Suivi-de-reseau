import unittest
from unittest.mock import patch
from src.core import runner

class TestRunner(unittest.TestCase):

    @patch("src.core.runner.scan_ips", return_value=[("host1", "192.168.1.1", "Active", 12)])
    def test_run_scan_threaded_without_ports(self, mock_scan):
        machines = [("host1", "192.168.1.1")]
        results = runner.run_scan(machines, use_async=False, threads=1, ports=False)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][2], "Active")
        self.assertEqual(results[0][-1], [])

    @patch("src.core.runner.async_scan_ips", return_value=[("host2", "192.168.1.2", "Active", 15)])
    def test_run_scan_async_without_ports(self, mock_async_scan):
        machines = [("host2", "192.168.1.2")]
        results = runner.run_scan(machines, use_async=True, threads=1, ports=False)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][2], "Active")
        self.assertEqual(results[0][-1], [])

    @patch("src.core.runner.scan_with_nmap", return_value=[(22, "ssh"), (80, "http")])
    @patch("src.core.runner.scan_ips", return_value=[("host3", "192.168.1.3", "Active", 8)])
    def test_run_scan_threaded_with_ports(self, mock_scan, mock_nmap):
        machines = [("host3", "192.168.1.3")]
        results = runner.run_scan(machines, use_async=False, threads=1, ports=True)
        self.assertEqual(results[0][-1], [(22, "ssh"), (80, "http")])

    @patch("src.core.runner.scan_with_nmap", return_value=[])
    @patch("src.core.runner.scan_ips", return_value=[("host4", "192.168.1.4", "Inactive", None)])
    def test_run_scan_threaded_with_ports_on_inactive_host(self, mock_scan, mock_nmap):
        machines = [("host4", "192.168.1.4")]
        results = runner.run_scan(machines, use_async=False, threads=1, ports=True)
        self.assertEqual(results[0][2], "Inactive")
        self.assertEqual(results[0][-1], [])

if __name__ == "__main__":
    unittest.main()
