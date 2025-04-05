"""Module contenant l'analyse des arguments pour le scanner réseau."""
import argparse


def parse_arguments():
    """
    Analyse les arguments passés en ligne de commande pour le scanner réseau.

    Returns:
        argparse.Namespace: Objet contenant tous les arguments analysés.
            - file (str|None): Chemin vers un fichier CSV d'entrées
              (optionnel).
            - range (str|None): Plage IP au format CIDR (optionnel).
            - threads (int): Nombre de threads pour le scan synchronisé.
            - use_async (bool): Active le scan asynchrone.
            - ports (bool): Active le scan complet des ports TCP via nmap.
    """
    parser = argparse.ArgumentParser(
        description="Network Scanner Tool"
    )
    parser.add_argument(
        "--file",
        help="Input CSV file with machine names and IPs"
    )
    parser.add_argument(
        "--range",
        help="CIDR IP range to scan (e.g. 192.168.1.0/24)"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=10,
        help="Number of threads for scanning"
    )
    parser.add_argument(
        "--async",
        dest="use_async",
        action="store_true",
        help="Use asynchronous scanning (asyncio)"
    )
    parser.add_argument(
        "--ports",
        action="store_true",
        help="Enable full TCP port scan (1–65535) on active hosts"
    )

    return parser.parse_args()
