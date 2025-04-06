"""
Utilitaires de parsing pour l'extraction de latence et la résolution DNS.
"""

import re
import socket


def extract_latency(stdout_str):
    """
    Extrait la latence moyenne d'un retour de commande ping.

    Fonctionne pour Linux/macOS, Windows FR/EN, avec prise en charge de
      plusieurs formats.

    Args:
        stdout_str (str): Sortie brute du ping.

    Returns:
        int or None: Latence moyenne en millisecondes, ou None si introuvable.
    """
    # Linux/macOS
    match = re.search(r"rtt [^=]+= [\d.]+/([\d.]+)/", stdout_str)
    if match:
        return int(float(match.group(1)))

    # Windows français
    match = re.search(r"Moyenne\s*=\s*(\d+)\s*ms", stdout_str)
    if match:
        return int(match.group(1))

    # Windows anglais
    match = re.search(r"Average\s*=\s*(\d+)\s*ms", stdout_str)
    if match:
        return int(match.group(1))

    # Fallback générique
    match = re.search(
        r"(temps|time)[=<]?=?\s*(\d+)\s*ms",
        stdout_str,
        re.IGNORECASE
        )
    if match:
        return int(match.group(2))

    return None


def resolve_hostname_if_needed(machine_name, ip):
    """
    Résout le nom DNS de l'hôte si machine_name est une adresse IP brute.

    Args:
        machine_name (str): Nom ou IP de la machine.
        ip (str): Adresse IP de la machine.

    Returns:
        str: Nom de la machine si résolu, sinon retourne l'IP.
    """
    if machine_name == ip:
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return ip
    return machine_name
