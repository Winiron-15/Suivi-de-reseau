import csv


def read_from_csv(filename):
    """
    Lit un fichier CSV et extrait les noms de machines et leurs IPs.

    Args:
        filename (str): Chemin vers le fichier CSV à lire.

    Returns:
        list of tuple: Liste de tuples (nom_machine, ip).
    """
    machines = []
    with open(filename, "r") as csvfile:
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
          sous forme (nom, ip, statut, ping).
        filename (str, optional): Nom du fichier de sortie.
          Par défaut "results.csv".

    Returns:
        None
    """
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Machine", "IP", "Status", "Ping (ms)"])
        writer.writerows(results)
