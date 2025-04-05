import subprocess
import re


def scan_with_nmap(ip):
    """
    Utilise nmap pour scanner tous les ports TCP sur une IP donnée.

    Args:
        ip (str): Adresse IP à scanner.

    Returns:
        list of tuple: Liste de tuples (port, service) détectés comme ouverts.
    """
    try:
        cmd = ["nmap", "-p", "1-65535", "-T5", ip]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
            )
        output = result.stdout

        open_ports = []
        for line in output.splitlines():
            match = re.match(r"^(\d+)/tcp\s+open\s+(\S+)", line)
            if match:
                port = int(match.group(1))
                service = match.group(2)
                open_ports.append((port, service))

        return open_ports

    except Exception as e:
        print(f"[ERROR] Nmap scan failed for {ip}: {e}")
        return []
