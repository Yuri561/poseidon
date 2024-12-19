import psutil

def fetch_system_info():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    return (
        f"CPU Usage: {cpu}%\n"
        f"Memory: {memory.percent}% used\n"
        f"Disk: {disk.percent}% used\n"
        f"Net Sent: {net.bytes_sent / 1024 / 1024:.2f} MB\n"
        f"Net Received: {net.bytes_recv / 1024 / 1024:.2f} MB\n"
    )
