from concurrent.futures import ThreadPoolExecutor
import platform
import subprocess
from datetime import datetime

def ping_ip(machine_name, ip):
    """Pings a single IP address and returns the result."""
    try:
        # Déterminer le système d'exploitation pour adapter la commande ping
        param = "-n" if platform.system().lower() == "windows" else "-c"
        timeout = "-w" if platform.system().lower() == "windows" else "-W"

        start = datetime.now()
        result = subprocess.run(
            ["ping", param, "3", timeout, "2", ip],  # Ping 3 fois avec un délai de 2 secondes
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Retourne la sortie en texte
        )
        end = datetime.now()

        if result.returncode == 0:
            # Si le ping réussit
            latency = (end - start).microseconds // 1000  # Convertir en millisecondes
            return machine_name, ip, "Active", latency
        else:
            # Si le ping échoue
            return machine_name, ip, "Inactive", None
    except Exception as e:
        # Gestion des exceptions
        return machine_name, ip, f"Error: {str(e)}", None



def scan_ips(machines, threads=10):
    """Scans a list of machines and returns their status."""
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(ping_ip, machine_name, ip): (machine_name, ip)
            for machine_name, ip in machines
        }
        for future in futures:
            results.append(future.result())
    return results
