import argparse

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Network Scanner Tool")
    parser.add_argument("--file", help="Input CSV file with machine names and IPs")
    parser.add_argument("--range", help="CIDR IP range to scan (e.g. 192.168.1.0/24)")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads for scanning")
    parser.add_argument("--async", dest="use_async", action="store_true", help="Use asynchronous scanning (asyncio)")
    parser.add_argument("--ports", action="store_true", help="Enable full TCP port scan (1–65535) on active hosts"
)

    return parser.parse_args()
