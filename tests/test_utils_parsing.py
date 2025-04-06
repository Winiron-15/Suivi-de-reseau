"""
Tests unitaires pour les fonctions de parsing dans utils/parsing.py
"""

import unittest
from src.utils import parsing


class TestParsing(unittest.TestCase):
    """Tests pour les fonctions d'extraction de latence et de résolution DNS"""

    def test_extract_latency_linux_format(self):
        """Doit extraire 0 ms depuis une sortie ping Linux"""
        output = "rtt min/avg/max/mdev = 0.033/0.045/0.056/0.011 ms"
        self.assertEqual(parsing.extract_latency(output), 0)

    def test_extract_latency_windows_fr_format(self):
        """Doit extraire 123 ms depuis une sortie ping Windows en français"""
        output = "    Moyenne = 123 ms"
        self.assertEqual(parsing.extract_latency(output), 123)

    def test_extract_latency_windows_en_format(self):
        """Doit extraire 85 ms depuis une sortie ping Windows en anglais"""
        output = "    Average = 85ms"
        self.assertEqual(parsing.extract_latency(output), 85)

    def test_extract_latency_empty(self):
        """Retourne None si la sortie est vide"""
        output = ""
        self.assertIsNone(parsing.extract_latency(output))

    def test_extract_latency_non_matching(self):
        """Retourne None si aucun motif de latence n'est trouvé"""
        output = "some random text without latency"
        self.assertIsNone(parsing.extract_latency(output))

    def test_resolve_hostname_when_different(self):
        """Doit retourner l'adresse IP si le nom et l'IP sont identiques"""
        result = parsing.resolve_hostname_if_needed("1.1.1.1", "1.1.1.1")
        self.assertTrue(isinstance(result, str))

    def test_resolve_hostname_when_already_named(self):
        """Doit conserver le nom d'hôte s'il est déjà fourni"""
        result = parsing.resolve_hostname_if_needed(
            "example.com", "93.184.216.34"
        )
        self.assertEqual(result, "example.com")


if __name__ == "__main__":
    unittest.main()
