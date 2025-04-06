"""
Tests unitaires pour le module core.ping.
"""

import unittest
from src.core import ping


class TestPingCommand(unittest.TestCase):
    """Test de la génération de commande ping selon l'OS."""
    def test_build_ping_command(self):
        """
        Vérifie que la commande ping contient bien l'IP et l'appel à ping.
        """
        ip = "192.168.1.1"
        command = ping.build_ping_command(ip)
        self.assertIn("ping", command)
        self.assertIn(ip, command)
