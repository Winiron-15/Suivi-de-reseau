"""
Utilitaires pour lire et écrire des fichiers CSV liés au scan réseau.
"""
import csv
import os


def read_from_csv(filename):
    """
    Lit un fichier CSV et extrait les noms de machines et leurs IPs.

    Args:
        filename (str): Chemin vers le fichier CSV à lire.

    Returns:
        list of tuple: Liste de tuples (nom_machine, ip).
    """
    machines = []
    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 2:
                machines.append((row[0], row[1]))
    return machines


def save_to_csv(results, filename="results.csv"):
    """
    Enregistre les résultats de scan dans un fichier CSV.

    Args:
        results (list of tuple): Résultats à enregistrer,
            sous forme (nom, ip, statut, latence, ports),
            où ports est une liste de tuples (port, service).
        filename (str, optional): Nom du fichier de sortie.
            Par défaut "results.csv".

    Returns:
        None
    """
    # Crée le dossier de sortie si nécessaire
    dir_path = os.path.dirname(filename)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Machine", "IP", "Status", "Ping (ms)", "Ports (Services)"])

        for machine, ip, status, latency, ports in results:
            port_str = " ".join(f"[{p} - {s}]" for p, s in ports) if ports else ""
            writer.writerow([machine, ip, status, latency, port_str])
