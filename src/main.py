from arguments import parse_arguments
from scanner import scan_ips
from utils import read_from_csv, save_to_csv
from async_scanner import async_scan_ips
import asyncio
import ipaddress

def main():
    args = parse_arguments()

    if hasattr(args, 'range') and args.range:
        try:
            network = ipaddress.ip_network(args.range, strict=False)
            machines = [(str(ip), str(ip)) for ip in network.hosts()]
            output_file = "data/results/range-results.csv"
        except ValueError as e:
            print(f"Invalid CIDR range: {e}")
            return
    elif hasattr(args, 'file') and args.file:
        machines = read_from_csv(args.file)
        output_file = "data/results/file-results.csv"
    else:
        print("You must provide either --file or --range")
        return

    print("Starting network scan...")
    if args.use_async:
        print("Using asynchronous scan...")
        results = asyncio.run(async_scan_ips(machines))
    else:
        print("Using threaded scan...")
        results = scan_ips(machines, args.threads)

    for result in results:
        print(f"Machine: {result[0]} - IP: {result[1]} - Status: {result[2]} - Ping: {result[3]} ms")

    save_to_csv(results, output_file)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()
