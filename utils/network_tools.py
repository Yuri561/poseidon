import subprocess
import platform

def ping_network(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.check_output(["ping", param, "4", ip], universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Ping failed for {ip}: {e}"

def traceroute(ip):
    command = "tracert" if platform.system().lower() == "windows" else "traceroute"
    try:
        result = subprocess.check_output([command, ip], universal_newlines=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Traceroute failed for {ip}: {e}"
