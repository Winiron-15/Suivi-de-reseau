import asyncio
from core.ping import build_ping_command
from utils.parsing import extract_latency, resolve_hostname_if_needed

async def async_ping_ip(machine_name, ip):
    """Asynchronously pings an IP address and returns the result."""
    try:
        cmd = build_ping_command(ip)

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        try:
            stdout_str = stdout.decode('utf-8')
        except UnicodeDecodeError:
            stdout_str = stdout.decode('latin1')

        if process.returncode == 0:
            latency = extract_latency(stdout_str)
            if machine_name == ip:
                try:
                    machine_name = resolve_hostname_if_needed(machine_name, ip)
                except Exception:
                    pass
            return (machine_name, ip, "Active", latency)
        else:
            return (machine_name, ip, "Inactive", None)
    except Exception as e:
        return (machine_name, ip, f"Error: {str(e)}", None)

async def async_scan_ips(machines):
    """Scans IPs concurrently using asyncio coroutines."""
    tasks = [async_ping_ip(machine_name, ip) for machine_name, ip in machines]
    return await asyncio.gather(*tasks)
