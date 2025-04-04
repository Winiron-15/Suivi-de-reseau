import csv

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
