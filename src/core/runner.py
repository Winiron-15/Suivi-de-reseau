import asyncio
from core.scanner_async import async_scan_ips
from core.scanner_threaded import scan_ips
from core.port_scanner import scan_with_nmap

def run_scan(machines, use_async=False, threads=10, ports=False):
    """
    Exécute le scan réseau et, si demandé, le scan des ports ouverts avec Nmap.

    Args:
        machines (list of tuple): Liste de tuples (nom_machine, ip).
        use_async (bool, optional): Si True, utilise asyncio. Sinon, multithread. Par défaut False.
        threads (int, optional): Nombre de threads pour le scan synchrone. Par défaut 10.
        ports (bool, optional): Si True, lance un scan complet des ports TCP sur les hôtes actifs.

    Returns:
        list of tuple: Résultats enrichis au format :
            (nom_machine, ip, status, latence, liste_ports)
            - liste_ports (list of tuple): [(port, service), ...] si --ports est activé
    """
    if use_async:
        print("Using asynchronous scan...")
        results = asyncio.run(async_scan_ips(machines))
    else:
        print("Using threaded scan...")
        results = scan_ips(machines, threads)

    if ports:
        print("Scanning all TCP ports with nmap on active IPs...")
        enriched_results = []
        for machine, ip, status, latency in results:
            if status == "Active":
                open_ports = scan_with_nmap(ip)
            else:
                open_ports = []
            enriched_results.append((machine, ip, status, latency, open_ports))
        return enriched_results

    return [(machine, ip, status, latency, []) for machine, ip, status, latency in results]
