from arguments import parse_arguments
from scanner import scan_ips
from utils import read_from_csv, save_to_csv

def main():
    args = parse_arguments()

    # Lire les IP et les noms des machines depuis le fichier CSV
    machines = read_from_csv(args.input)

    print("Starting network scan...")
    results = scan_ips(machines, args.threads)

    for result in results:
        print(f"Machine: {result[0]} - IP: {result[1]} - Status: {result[2]} - Ping: {result[3]} ms")

    save_to_csv(results, args.output)
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
