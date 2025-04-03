from concurrent.futures import ThreadPoolExecutor
import platform
import subprocess
from datetime import datetime
import socket  # Ajoute ça en haut du fichier
import re

def ping_ip(machine_name, ip):
    """Pings a single IP address and returns the result."""
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        timeout = "-w" if platform.system().lower() == "windows" else "-W"

        start = datetime.now()
        result = subprocess.run(
            ["ping", param, "3", timeout, "2", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        end = datetime.now()

        if result.returncode == 0:
            latency = (end - start).microseconds // 1000
            if machine_name == ip:
                machine_name = get_hostname_from_nmap(ip)
            return machine_name, ip, "Active", latency
        else:
            return machine_name, ip, "Inactive", None
    except Exception as e:
        return machine_name, ip, f"Error: {str(e)}", None

def get_hostname_from_nmap(ip):
    """Uses nmap to try and get the hostname of a given IP."""
    try:
        result = subprocess.run(
            ["nmap", "-sP", ip],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        match = re.search(r"Nmap scan report for (.+)", result.stdout)
        if match:
            hostname = match.group(1).strip()
            return hostname
    except Exception:
        pass
    return ip  # fallback

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
