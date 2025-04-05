import platform


def build_ping_command(ip: str, count: int = 3, timeout: int = 2) -> list:
    """
    Construit une commande ping adaptée au système d'exploitation
      (Windows/Linux).

    Args:
        ip (str): Adresse IP à pinger.
        count (int, optional): Nombre de requêtes ICMP à envoyer. Par défaut 3.
        timeout (int, optional): Durée maximale (en secondes) d'attente
          d'une réponse. Par défaut 2.

    Returns:
        list: Liste représentant la commande ping à exécuter avec subprocess.
    """
    is_windows = platform.system().lower() == "windows"
    param = "-n" if is_windows else "-c"
    timeout_flag = "-w" if is_windows else "-W"

    return [
        "ping", param, str(count),
        timeout_flag, str(timeout),
        ip
    ]
