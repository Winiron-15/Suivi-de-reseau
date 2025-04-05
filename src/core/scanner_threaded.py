from concurrent.futures import ThreadPoolExecutor
from core.ping import build_ping_command
from utils.parsing import extract_latency, resolve_hostname_if_needed
import subprocess

def ping_ip(machine_name, ip):
    """
    Envoie un ping à une adresse IP et retourne son statut.

    Args:
        machine_name (str): Nom de la machine (ou IP si inconnu).
        ip (str): Adresse IP à tester.

    Returns:
        tuple: (nom_machine, ip, status, latence)
            - status (str): "Active", "Inactive" ou "Error: <msg>"
            - latence (int|None): Temps de réponse moyen en ms si disponible
    """
    try:
        cmd = build_ping_command(ip)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            stdout_str = result.stdout
            latency = extract_latency(stdout_str)
            if machine_name == ip:
                machine_name = resolve_hostname_if_needed(machine_name, ip)
            return machine_name, ip, "Active", latency
        else:
            return machine_name, ip, "Inactive", None
    except Exception as e:
        return machine_name, ip, f"Error: {str(e)}", None

def scan_ips(machines, threads=10):
    """
    Scanne une liste de machines via des threads.

    Args:
        machines (list of tuple): Liste de tuples (nom_machine, ip).
        threads (int, optional): Nombre de threads à utiliser. Défaut : 10.

    Returns:
        list of tuple: Résultats du ping pour chaque machine, au format
            (nom_machine, ip, status, latence)
    """
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(ping_ip, machine_name, ip): (machine_name, ip)
            for machine_name, ip in machines
        }
        for future in futures:
            results.append(future.result())
    return results
