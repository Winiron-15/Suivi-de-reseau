# Tests pour le module 'arguments'
# -------- test_arguments.py --------

import unittest
from unittest.mock import patch
import sys
import src.arguments as arguments


class TestArguments(unittest.TestCase):
    def test_default_arguments(self):
        test_args = ["main.py", "--range", "192.168.1.0/30"]
        with patch.object(sys, 'argv', test_args):
            args = arguments.parse_arguments()
            self.assertEqual(args.range, "192.168.1.0/30")
            self.assertEqual(args.threads, 10)
            self.assertFalse(args.use_async)
            self.assertFalse(args.ports)
