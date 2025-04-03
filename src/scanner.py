from concurrent.futures import ThreadPoolExecutor
import platform
import subprocess
import socket
from datetime import datetime

def resolve_hostname(ip):
    """Try to resolve the hostname using reverse DNS."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ip

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
                machine_name = resolve_hostname(ip)
            return machine_name, ip, "Active", latency
        else:
            return machine_name, ip, "Inactive", None
    except Exception as e:
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
