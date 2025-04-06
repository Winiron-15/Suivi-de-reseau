"""
Tests unitaires pour le module arguments.
"""

import sys
import unittest

from unittest.mock import patch
from src.arguments import parse_arguments


class TestArguments(unittest.TestCase):
    """Test des arguments de ligne de commande."""
    def test_default_arguments(self):
        """Teste la valeur par défaut des arguments."""
        test_args = ["main.py", "--range", "192.168.1.0/30"]
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            self.assertEqual(args.range, "192.168.1.0/30")
            self.assertEqual(args.threads, 10)
            self.assertFalse(args.use_async)
            self.assertFalse(args.ports)
