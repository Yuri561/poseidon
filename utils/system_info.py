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
# import os
# import shutil
#
# def organize_files(directory, categories, delete_empty_folders, dry_run, organize_by_date):
#     if not os.path.exists(directory):
#         return f"Directory {directory} does not exist."
#
#     log = []
#     for folder, extensions in categories.items():
#         folder_path = os.path.join(directory, folder)
#         if not os.path.exists(folder_path) and not dry_run:
#             os.makedirs(folder_path)
#
#         for filename in os.listdir(directory):
#             file_path = os.path.join(directory, filename)
#             if os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in extensions):
#                 if not dry_run:
#                     shutil.move(file_path, folder_path)
#                 log.append(f"Moved {filename} to {folder}")
#
#     return "\n".join(log)
