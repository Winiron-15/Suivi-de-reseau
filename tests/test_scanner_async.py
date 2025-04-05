import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from src.core import scanner_async

class TestScannerAsync(unittest.IsolatedAsyncioTestCase):

    @patch("src.core.scanner_async.async_ping_ip", new_callable=AsyncMock)
    async def test_async_scan_ips_success(self, mock_ping):
        mock_ping.return_value = ("192.168.1.10", "192.168.1.10", "Active", 10)
        machines = [("192.168.1.10", "192.168.1.10")]
        result = await scanner_async.async_scan_ips(machines)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][2], "Active")

    @patch("src.core.scanner_async.async_ping_ip", new_callable=AsyncMock)
    async def test_async_scan_ips_failure(self, mock_ping):
        mock_ping.return_value = ("192.168.1.10", "192.168.1.10", "Inactive", None)
        machines = [("192.168.1.10", "192.168.1.10")]
        result = await scanner_async.async_scan_ips(machines)
        self.assertEqual(result[0][2], "Inactive")

    async def test_async_ping_ip_invalid(self):
        result = await scanner_async.async_ping_ip("unknown", "256.256.256.256")
        self.assertEqual(result[2], "Inactive")

if __name__ == "__main__":
    unittest.main()