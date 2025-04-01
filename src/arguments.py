import argparse

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Network Scanner Tool")
    parser.add_argument("--file", required=True, help="Input CSV file with machine names and IPs")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads for scanning")
    return parser.parse_args()
