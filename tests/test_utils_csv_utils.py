"""
Tests unitaires pour les fonctions CSV dans utils/csv_utils.py
"""

import unittest
import os
from src.utils import csv_utils


class TestCSVUtils(unittest.TestCase):
    """Tests pour les fonctions de lecture de fichiers CSV"""

    def setUp(self):
        """Crée un fichier CSV de test temporaire"""
        self.test_file = "data/test_machines.csv"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Machine,IP\n")
            f.write("Serveur1,192.168.1.10\n")
            f.write("Serveur2,192.168.1.20\n")

    def tearDown(self):
        """Supprime le fichier CSV temporaire"""
        os.remove(self.test_file)

    def test_read_from_csv(self):
        """Teste que les données sont correctement lues du CSV"""
        result = csv_utils.read_from_csv(self.test_file)
        self.assertEqual(
            result,
            [
                ("Serveur1", "192.168.1.10"),
                ("Serveur2", "192.168.1.20")
            ]
        )


if __name__ == "__main__":
    unittest.main()
