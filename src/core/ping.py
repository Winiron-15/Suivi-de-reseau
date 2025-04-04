import platform

def build_ping_command(ip: str, count: int = 3, timeout: int = 2) -> list:
    """Construit la commande ping selon le système."""
    is_windows = platform.system().lower() == "windows"
    param = "-n" if is_windows else "-c"
    timeout_flag = "-w" if is_windows else "-W"
    return ["ping", param, str(count), timeout_flag, str(timeout), ip]
