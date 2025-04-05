import unittest
from src.core import ping
import platform

class TestPingCommand(unittest.TestCase):
    def test_build_ping_command(self):
        ip = "192.168.1.1"
        command = ping.build_ping_command(ip)
        self.assertIn("ping", command)
        self.assertIn(ip, command)