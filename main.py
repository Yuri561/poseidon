import os
import shutil
import psutil
import networkscan
import csv
import time
import threading
import subprocess
import customtkinter as ctk
from tkinter import scrolledtext


# Notification function (adds text to Home log)
def notify(message):
    log_textbox.insert(ctk.END, message + "\n")
    log_textbox.see(ctk.END)


# File Organizer Function (Added file organization by date)
def organize_files(directory, categories, delete_empty_folders, dry_run, organize_by_date):
    if not os.path.exists(directory):
        notify(f"Directory {directory} does not exist.")
        return

    moved_files = []
    log_output = []
    total_files = len(os.listdir(directory))

    progress.set(0)  # Reset progress bar
    for folder, extensions in categories.items():
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path) and not dry_run:
            os.makedirs(folder_path)

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1]
                if file_ext in extensions:
                    log_message = f"File '{filename}' would be moved to '{folder}'" if dry_run else f"Moved '{filename}' to '{folder}'"
                    log_output.append(log_message)

                    if not dry_run:
                        if organize_by_date:
                            timestamp = os.path.getmtime(file_path)
                            folder_by_date = os.path.join(directory, time.strftime('%Y-%m-%d', time.gmtime(timestamp)))
                            if not os.path.exists(folder_by_date):
                                os.makedirs(folder_by_date)
                            shutil.move(file_path, folder_by_date)
                        else:
                            shutil.move(file_path, folder_path)
                        moved_files.append((file_path, folder_path))

                    progress.set(progress.get() + 1)

    notify("\n".join(log_output))
    if delete_empty_folders and not dry_run:
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                dir_path = os.path.join(root, d)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    notify(f"Deleted empty folder {dir_path}")

    notify("File organization completed." if not dry_run else "Dry run completed.")
    return moved_files


# Ping Network Function (Now captures and shows full ping output)
def ping_network(ip_address):
    try:
        result = subprocess.run(['ping', ip_address, '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            notify(result.stdout)  # Display successful ping output
        else:
            notify(result.stdout + result.stderr)  # Display failed ping output
    except Exception as e:
        notify(f"Ping Error: {str(e)}")


# Traceroute Function to track route to a network device
def traceroute(ip_address):
    result = subprocess.run(['tracert', ip_address], stdout=subprocess.PIPE)
    notify(result.stdout.decode('utf-8'))


# SNMP Device Discovery Using Net-SNMP
def snmp_device_discovery(ip_address, community='public'):
    try:
        command = ['snmpwalk', '-v2c', '-c', community, ip_address, '1.3.6.1.2.1.1.1.0']  # OID for sysDescr
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.stderr:
            notify(f"SNMP Error: {result.stderr}")
        else:
            notify(f"SNMP Response: {result.stdout}")
    
    except Exception as e:
        notify(f"An error occurred: {str(e)}")


# Scanning the network using CIDR notation with detailed host info and CSV export
def scan_network(ip_scan):
    try:
        my_scan = networkscan.Networkscan(ip_scan)
        my_scan.run()

        hosts_info = []
        if my_scan.list_of_hosts_found:
            for host in my_scan.list_of_hosts_found:
                host_info = {
                    'IP': host['ip'],
                    'MAC': host['mac'] if 'mac' in host else 'Unknown',
                    'Vendor': host['vendor'] if 'vendor' in host else 'Unknown'
                }
                hosts_info.append(host_info)
                notify(f"Host found: {host_info['IP']}, MAC: {host_info['MAC']}, Vendor: {host_info['Vendor']}")
        else:
            notify("No hosts found on the network.")

        # Save results to CSV
        with open('network_scan_results.csv', 'w', newline='') as csvfile:
            fieldnames = ['IP', 'MAC', 'Vendor']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(hosts_info)

        notify("Network scan completed.")
    except Exception as e:
        notify(f"An error occurred while scanning: {str(e)}")


# Real-time System Info Function
def get_system_info():
    while True:
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        net_io = psutil.net_io_counters()

        info = (
            f"CPU Usage: {cpu_usage}%\n"
            f"Memory Usage: {memory_info.percent}%\n"
            f"Disk Usage: {disk_info.percent}%\n"
            f"Network Sent: {net_io.bytes_sent / 1024 / 1024:.2f} MB\n"
            f"Network Received: {net_io.bytes_recv / 1024 / 1024:.2f} MB"
        )
        notify(info)
        time.sleep(2)  # Refresh every 2 seconds


# Thread function for real-time monitoring
def run_system_monitoring():
    threading.Thread(target=get_system_info, daemon=True).start()


# Initialize CustomTkinter
ctk.set_appearance_mode("dark")  # Enable dark mode
ctk.set_default_color_theme("blue")

app = ctk.CTk()  # Create window
app.title("Poseidon App")
app.geometry("800x600")

# Tab View
tab_view = ctk.CTkTabview(app, width=780, height=550)
tab_view.pack(pady=10)

# Home Tab (Report Screen)
home_tab = tab_view.add("Home")
log_textbox = scrolledtext.ScrolledText(home_tab, width=90, height=25, bg="black", fg="white")
log_textbox.pack(pady=20)

# Network Tab
network_tab = tab_view.add("Network")

network_frame = ctk.CTkFrame(network_tab)
network_frame.pack(pady=20)

ctk.CTkLabel(network_frame, text="Ping IP:").grid(row=0, column=0, padx=10, pady=10)
ping_input = ctk.CTkEntry(network_frame)
ping_input.grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(network_frame, text="Ping", command=lambda: ping_network(ping_input.get())).grid(row=0, column=2)

ctk.CTkLabel(network_frame, text="Traceroute IP:").grid(row=1, column=0, padx=10, pady=10)
traceroute_input = ctk.CTkEntry(network_frame)
traceroute_input.grid(row=1, column=1, padx=10, pady=10)
ctk.CTkButton(network_frame, text="Traceroute", command=lambda: traceroute(traceroute_input.get())).grid(row=1, column=2)

ctk.CTkLabel(network_frame, text="SNMP Device IP:").grid(row=2, column=0, padx=10, pady=10)
snmp_input = ctk.CTkEntry(network_frame)
snmp_input.grid(row=2, column=1, padx=10, pady=10)
ctk.CTkButton(network_frame, text="Discover SNMP", command=lambda: snmp_device_discovery(snmp_input.get())).grid(row=2, column=2)

# Network Scan Section
ctk.CTkLabel(network_frame, text="Network Scan (CIDR):").grid(row=3, column=0, padx=10, pady=10)
scan_input = ctk.CTkEntry(network_frame)
scan_input.grid(row=3, column=1, padx=10, pady=10)
ctk.CTkButton(network_frame, text="Scan Network", command=lambda: scan_network(scan_input.get())).grid(row=3, column=2)

# Organizer Tab
organizer_tab = tab_view.add("Organizer")

organizer_frame = ctk.CTkFrame(organizer_tab)
organizer_frame.pack(pady=20)

ctk.CTkLabel(organizer_frame, text="Select Directory:").grid(row=0, column=0, padx=10, pady=10)
directory_input = ctk.CTkEntry(organizer_frame)
directory_input.grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(organizer_frame, text="Browse", command=lambda: directory_input.insert(0, ctk.filedialog.askdirectory())).grid(row=0, column=2)

delete_empty_folders = ctk.CTkCheckBox(organizer_frame, text="Delete Empty Folders")
delete_empty_folders.grid(row=1, column=0, padx=10, pady=10)
dry_run = ctk.CTkCheckBox(organizer_frame, text="Dry Run")
dry_run.grid(row=1, column=1, padx=10, pady=10)
organize_by_date = ctk.CTkCheckBox(organizer_frame, text="Organize by Date")
organize_by_date.grid(row=1, column=2, padx=10, pady=10)

ctk.CTkButton(organizer_frame, text="Organize Files", command=lambda: organize_files(
    directory_input.get(),
    {
        'Images': ['.png', '.jpg', '.jpeg', '.gif'],
        'Documents': ['.pdf', '.docx', '.txt', '.xls', '.xlsx'],
        'Videos': ['.mp4', '.avi', '.mkv'],
        'Audio': ['.mp3', '.wav', '.flac'],
        'Compressed': ['.zip', '.rar', '.7z'],
        'Executables': ['.exe', '.bat', '.sh']
    },
    delete_empty_folders.get(), dry_run.get(), organize_by_date.get()
)).grid(row=2, column=1, pady=20)

progress = ctk.DoubleVar()
progress_bar = ctk.CTkProgressBar(organizer_frame, variable=progress)
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Start the application
app.mainloop()
