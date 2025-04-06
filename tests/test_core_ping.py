# Tests pour le module 'core/ping'
# -------- test_ping.py --------

import unittest
from src.core import ping


class TestPingCommand(unittest.TestCase):
    def test_build_ping_command(self):
        ip = "192.168.1.1"
        command = ping.build_ping_command(ip)
        self.assertIn("ping", command)
        self.assertIn(ip, command)
