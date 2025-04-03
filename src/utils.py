import csv
import socket

def read_from_csv(filename):
    """Reads machine names and IPs from a CSV file."""
    machines = []
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 2:
                machines.append((row[0], row[1]))
    return machines


def save_to_csv(results, filename="results.csv"):
    """Saves scan results to a CSV file."""
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Machine", "IP", "Status", "Ping (ms)"])
        writer.writerows(results)

import re

def extract_latency(stdout_str):
    """Extracts average ping latency from ping output (Linux or Windows, FR or EN)."""
    # Linux/macOS
    match = re.search(r"rtt [^\n=]+= [\d.]+/([\d.]+)/", stdout_str)
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

    # Fallback
    match = re.search(r"(temps|time)[=<]?\s*=?\s*(\d+)\s*ms", stdout_str, re.IGNORECASE)
    if match:
        return int(match.group(2))

    return None

def resolve_hostname_if_needed(machine_name, ip):
    """Résout le nom de la machine si machine_name est une IP."""
    if machine_name == ip:
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return ip
    return machine_name