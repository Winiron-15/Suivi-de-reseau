import unittest
import sys
from unittest.mock import patch, mock_open
from src import main

class TestMain(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("src.main.read_from_csv", return_value=[("host1", "192.168.1.1")])
    @patch("src.core.runner.scan_with_nmap", return_value=[(8080, "http")])
    @patch("src.main.run_scan", return_value=[("host1", "192.168.1.1", "up", 10, [(8080, "http")])])
    @patch("src.main.check_nmap_installed")
    def test_file_mode_with_ports(self, mock_nmap, mock_run_scan, mock_scan_nmap, mock_csv, mock_file):
        import subprocess, time
        server = subprocess.Popen(['python', '-m', 'http.server', '8080'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        test_args = ["main.py", "--file", "data/machines.csv", "--ports"]
        with patch.object(sys, "argv", test_args):
            main.main()
        server.terminate()
        server.wait()
        mock_nmap.assert_called_once()
        mock_csv.assert_called_once_with("data/machines.csv")
        mock_run_scan.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("src.core.runner.scan_with_nmap", return_value=[(22, "ssh")])
    @patch("src.main.run_scan", return_value=[("192.168.1.2", "192.168.1.2", "up", 5, [])])
    @patch("src.main.check_nmap_installed")
    def test_range_mode(self, mock_nmap, mock_run_scan, mock_scan_nmap, mock_file):
        test_args = ["main.py", "--range", "192.168.1.0/30"]
        with patch.object(sys, "argv", test_args):
            main.main()
        mock_run_scan.assert_called_once()

    @patch("src.core.runner.scan_with_nmap", return_value=[(22, "ssh")])
    @patch("src.main.logger")
    def test_no_argument(self, mock_logger, mock_scan_nmap):
        test_args = ["main.py"]
        with patch.object(sys, "argv", test_args):
            main.main()
        mock_logger.error.assert_called_with("You must provide either --file or --range")

    @patch("src.core.runner.scan_with_nmap", return_value=[(22, "ssh")])
    @patch("src.main.logger")
    def test_invalid_cidr(self, mock_logger, mock_scan_nmap):
        test_args = ["main.py", "--range", "invalid_cidr"]
        with patch.object(sys, "argv", test_args):
            main.main()
        self.assertIn("Invalid CIDR range", mock_logger.error.call_args[0][0])

if __name__ == "__main__":
    unittest.main()
