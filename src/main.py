from arguments import parse_arguments
from core.runner import run_scan
from utils.csv_utils import read_from_csv
from utils.logger import setup_logger
import ipaddress
import csv
import shutil
import sys


logger = setup_logger()


def check_nmap_installed():
    """
    Vérifie que la commande 'nmap' est bien installée sur le système.
    Arrête l'exécution du programme avec un message d'erreur
    si nmap est introuvable.
    """
    logger.info("Vérification de la présence de nmap...")
    if shutil.which("nmap") is None:
        logger.error(
            "Nmap n'est pas installé ou n'est pas dans le PATH. "
            "Veuillez l'installer pour utiliser l'option --ports."
        )
        sys.exit(1)


def main():
    """
    Point d'entrée principal du script. Traite les arguments,
    lance le scan et sauvegarde les résultats.
    """
    args = parse_arguments()

    if args.ports:
        check_nmap_installed()

    if hasattr(args, 'range') and args.range:
        try:
            network = ipaddress.ip_network(args.range, strict=False)
            machines = [(str(ip), str(ip)) for ip in network.hosts()]
            output_file = "data/results/range-results.csv"
        except ValueError as e:
            logger.error(f"Invalid CIDR range: {e}")
            return

    elif hasattr(args, 'file') and args.file:
        machines = read_from_csv(args.file)
        output_file = "data/results/file-results.csv"
    else:
        logger.error("You must provide either --file or --range")
        return

    logger.info("Appuyez sur Ctrl + C à tout moment pour interrompre le scan.")

    try:
        logger.info("Starting network scan...")
        results = run_scan(
            machines,
            use_async=args.use_async,
            threads=args.threads,
            ports=args.ports
        )
    except KeyboardInterrupt:
        logger.warning("Scan interrompu par l'utilisateur (Ctrl + C).")
        return

    for machine, ip, status, latency, ports in results:
        port_list_str = (
            ", ".join(f"{p} - {s}" for p, s in ports) if ports else ""
        )
        logger.info(
            f"Machine: {machine} - IP: {ip} - Status: {status} - "
            f"Ping: {latency} ms - Ports: {port_list_str}"
        )

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Machine", "IP", "Status", "Ping (ms)", "Ports"])
        for machine, ip, status, latency, ports in results:
            port_str = " ".join(f"[{p} - {s}]" for p, s in ports)
            writer.writerow([machine, ip, status, latency, port_str])


if __name__ == "__main__":
    main()
