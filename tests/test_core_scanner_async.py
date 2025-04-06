# Tests pour le module 'core/scanner_async'

import unittest

from unittest.mock import patch, AsyncMock
from src.core import scanner_async


class TestScannerAsync(unittest.IsolatedAsyncioTestCase):

    @patch(
        "src.core.scanner_async.async_ping_ip",
        new_callable=AsyncMock
    )
    async def test_async_scan_ips_success(self, mock_ping):
        mock_ping.return_value = (
            "192.168.1.10",
            "192.168.1.10",
            "Active",
            10
        )
        machines = [("192.168.1.10", "192.168.1.10")]
        result = await scanner_async.async_scan_ips(machines)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][2], "Active")

    @patch(
        "src.core.scanner_async.async_ping_ip",
        new_callable=AsyncMock
    )
    async def test_async_scan_ips_failure(self, mock_ping):
        mock_ping.return_value = (
            "192.168.1.10",
            "192.168.1.10",
            "Inactive",
            None
        )
        machines = [("192.168.1.10", "192.168.1.10")]
        result = await scanner_async.async_scan_ips(machines)
        self.assertEqual(result[0][2], "Inactive")

    async def test_async_ping_ip_invalid(self):
        result = await scanner_async.async_ping_ip(
            "unknown",
            "256.256.256.256"
        )
        self.assertEqual(result[2], "Inactive")


class TestScannerAsyncExtended(unittest.IsolatedAsyncioTestCase):

    @patch(
        "src.core.scanner_async.resolve_hostname_if_needed",
        side_effect=Exception("DNS failure")
    )
    @patch(
        "src.core.scanner_async.extract_latency",
        return_value=42
    )
    async def test_resolve_hostname_exception(
        self,
        mock_latency,
        mock_resolve
    ):
        process_mock = AsyncMock()
        process_mock.returncode = 0
        process_mock.communicate.return_value = (
            b"ping output",
            b""
        )

        with patch(
            "src.core.scanner_async.build_ping_command",
            return_value=["ping", "host"]
        ), patch(
            "asyncio.create_subprocess_exec",
            return_value=process_mock
        ):
            result = await scanner_async.async_ping_ip(
                "127.0.0.1",
                "127.0.0.1"
            )
            self.assertEqual(result[2], "Active")

    async def test_ping_returncode_nonzero(self):
        process_mock = AsyncMock()
        process_mock.returncode = 1
        process_mock.communicate.return_value = (b"", b"")

        with patch(
            "src.core.scanner_async.build_ping_command",
            return_value=["ping", "host"]
        ), patch(
            "asyncio.create_subprocess_exec",
            return_value=process_mock
        ):
            result = await scanner_async.async_ping_ip(
                "host",
                "192.168.1.1"
            )
            self.assertEqual(result[2], "Inactive")

    async def test_decode_utf8_then_latin1(self):
        process_mock = AsyncMock()
        process_mock.returncode = 0
        process_mock.communicate.return_value = (
            b"non_utf8_\x96_bytes",
            b""
        )

        with patch(
            "src.core.scanner_async.build_ping_command",
            return_value=["ping", "host"]
        ), patch(
            "src.core.scanner_async.extract_latency",
            return_value=33
        ), patch(
            "asyncio.create_subprocess_exec",
            return_value=process_mock
        ):
            result = await scanner_async.async_ping_ip(
                "host",
                "1.1.1.1"
            )
            self.assertEqual(result[2], "Active")
            self.assertEqual(result[3], 33)

    async def test_async_ping_ip_exception(self):
        with patch(
            "src.core.scanner_async.build_ping_command",
            side_effect=Exception("Boom")
        ):
            result = await scanner_async.async_ping_ip(
                "fail",
                "1.2.3.4"
            )
            self.assertIn("Error", result[2])


if __name__ == "__main__":
    unittest.main()
