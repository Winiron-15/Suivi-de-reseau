from arguments import parse_arguments
from scanner import scan_ips
from utils import read_from_csv, save_to_csv
import ipaddress
import os
import shutil
import sys

def check_nmap_installed():
    if shutil.which("nmap") is None:
        # Cas spécial : nmap est installé mais pas visible dans ce shell
        custom_paths = [
            r"C:\Program Files (x86)\Nmap",
            r"C:\Program Files\Nmap"
        ]
        for path in custom_paths:
            full = os.path.join(path, "nmap.exe")
            if os.path.isfile(full):
                os.environ["PATH"] += os.pathsep + path
                return  # Nmap trouvé, on continue

        print("Erreur : nmap n'est pas installé ou introuvable dans le PATH.")
        print("Veuillez l’installer ou ajouter le dossier de Nmap à la variable PATH.")
        sys.exit(1)

def main():
    check_nmap_installed()
    args = parse_arguments()

    if hasattr(args, 'range') and args.range:
        try:
            network = ipaddress.ip_network(args.range, strict=False)
            machines = [(str(ip), str(ip)) for ip in network.hosts()]
            output_file = "data/scan-results.csv"
        except ValueError as e:
            print(f"Invalid CIDR range: {e}")
            return
    elif hasattr(args, 'file') and args.file:
        machines = read_from_csv(args.file)
        output_file = "data/results.csv"
    else:
        print("You must provide either --file or --range")
        return

    print("Starting network scan...")
    results = scan_ips(machines, args.threads)

    for result in results:
        print(f"Machine: {result[0]} - IP: {result[1]} - Status: {result[2]} - Ping: {result[3]} ms")

    save_to_csv(results, output_file)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()
