import unittest
import os
from unittest.mock import patch
from src.utils import csv_utils

class TestCSVUtils(unittest.TestCase):
    def setUp(self):
        self.test_file = "data/test_machines.csv"
        with open(self.test_file, "w") as f:
            f.write("Machine,IP\n")
            f.write("Serveur1,192.168.1.10\n")
            f.write("Serveur2,192.168.1.20\n")

    def tearDown(self):
        os.remove(self.test_file)

    def test_read_from_csv(self):
        result = csv_utils.read_from_csv(self.test_file)
        self.assertEqual(result, [("Serveur1", "192.168.1.10"), ("Serveur2", "192.168.1.20")])
