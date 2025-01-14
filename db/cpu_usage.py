import psutil
from math import floor

# Get CPU usage
cpu_percent = floor(psutil.cpu_percent(interval=1))  # Get CPU usage percentage over 1 second
print("CPU Usage:", cpu_percent, "%")

# Get memory usage
memory = psutil.virtual_memory()
total_memory = floor(memory.available / (1024 ** 3))  # Available memory in GB
print("Available Memory:", total_memory, "GB")

# Get disk usage for the C: drive
disk = psutil.disk_usage('C:\\')  #the C: drive
disk_used = floor(disk.free / (1024 ** 3))  # Free disk space in GB
print("Free Disk Space on C:", disk_used, "GB")
