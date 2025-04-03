from concurrent.futures import ThreadPoolExecutor
from utils import extract_latency
from utils import resolve_hostname_if_needed
import platform
import subprocess

def ping_ip(machine_name, ip):
    """Pings a single IP address and returns the result."""
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        timeout = "-w" if platform.system().lower() == "windows" else "-W"

        result = subprocess.run(
            ["ping", param, "3", timeout, "2", ip],
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
