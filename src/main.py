from arguments import parse_arguments
from core.runner import run_scan
from utils.csv_utils import read_from_csv
from utils.logger import setup_logger
import ipaddress

logger = setup_logger()

def main():
    args = parse_arguments()

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

    logger.info("Starting network scan...")
    results = run_scan(
        machines,
        use_async=args.use_async,
        threads=args.threads,
        ports=args.ports
    )

    for machine, ip, status, latency, ports in results:
        if ports:
            port_list_str = ", ".join(f"{p} - {s}" for p, s in ports)
        else:
            port_list_str = ""
        logger.info(f"Machine: {machine} - IP: {ip} - Status: {status} - Ping: {latency} ms - Ports: {port_list_str}")

    # Sauvegarde CSV avec services
    import csv
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Machine", "IP", "Status", "Ping (ms)", "Ports"])
        for machine, ip, status, latency, ports in results:
            port_str = " ".join(f"[{p} - {s}]" for p, s in ports)
            writer.writerow([machine, ip, status, latency, port_str])

    logger.info(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
