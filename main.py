import os
import shutil
import pyttsx3
import psutil
import networkscan
from PySimpleGUI import Window, Print, FolderBrowse, popup_no_buttons, Button, WINDOW_CLOSED, InputText, Output, Text, \
    ProgressBar, Checkbox, Column, Multiline

# Initialize text-to-speech
engine = pyttsx3.init()


# Notification Reader Function
def notify_and_read(message):
    popup_no_buttons(message, title="Poseidon Notification", auto_close=True, auto_close_duration=3)
    engine.say(message)
    engine.runAndWait()


# File Organizer Function
def organize_files(directory, categories, delete_empty_folders, dry_run):
    if not os.path.exists(directory):
        notify_and_read(f"Directory {directory} does not exist.")
        return

    moved_files = []
    log_output = []
    total_files = len(os.listdir(directory))
    window['progress_bar'].update(max=total_files)
    progress = 0

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
                        shutil.move(file_path, folder_path)
                        moved_files.append((file_path, folder_path))
                    progress += 1
                    window['progress_bar'].update(progress)

    window['log_output'].update('\n'.join(log_output))

    if delete_empty_folders and not dry_run:
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                dir_path = os.path.join(root, d)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    notify_and_read(f"Deleted empty folder {dir_path}")

    notify_and_read("File organization completed." if not dry_run else "Dry run completed.")

    return moved_files


# Undo the last organization
def undo_last_operation(moved_files):
    for src, dest in moved_files:
        filename = os.path.basename(src)
        original_path = os.path.join(os.path.dirname(dest), filename)
        shutil.move(os.path.join(dest, filename), original_path)
        notify_and_read(f"Undid move for {filename}")


# Ping Network Function
def ping_network(ip_address):
    response = os.system(f"ping {ip_address} -n 1")
    if response == 0:
        notify_and_read(f"Successfully pinged {ip_address}")
    else:
        notify_and_read(f"Failed to ping {ip_address}. Check the IP address and try again.")


# Scanning the network using CIDR notation
def scan_network(ip_scan):
    try:
        my_scan = networkscan.Networkscan(ip_scan)
        my_scan.run()

        if my_scan.list_of_hosts_found:
            for network in my_scan.list_of_hosts_found:
                Print(f"Host found: {network}")
        else:
            Print("No hosts found on the network.")
        notify_and_read("Network scan completed.")
    except Exception as e:
        notify_and_read(f"An error occurred while scanning: {str(e)}")


# System Info Function
def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    info = (
        f"CPU Usage: {cpu_usage}%\n"
        f"Memory Usage: {memory_info.percent}%\n"
        f"Disk Usage: {disk_info.percent}%"
    )
    notify_and_read(info)
    Print(info)


# Main GUI Function
def create_gui():
    # Define the layout of the app
    file_organizer_section = [
        [Text('Organize Files')],  # Replaces the title in Column
        [InputText(key='directory_input', size=(40, 1)), FolderBrowse('Browse')],
        [Checkbox('Delete empty folders', default=False, key='delete_empty_folders')],
        [Checkbox('Dry Run (Preview Only)', default=True, key='dry_run')],
        [Button('Organize Files'), Button('Undo Last Operation')],
        [ProgressBar(max_value=100, orientation='h', size=(20, 20), key='progress_bar')],
        [Multiline(size=(60, 10), key='log_output', disabled=True)]
    ]

    network_section = [
        [Text('Ping Network')],
        [InputText('8.8.8.8', key='ip_input', size=(40, 1)), Button('Ping IP')],
        [Text('Network Scan (CIDR Notation)')],
        [InputText('192.168.1.0/24', key='network_input', size=(40, 1)), Button('Scan Network')]
    ]

    system_info_section = [
        [Text('System Info')],
        [Button('Get System Info')]
    ]

    layout = [
        [Text('Poseidon App', font=('Helvetica', 16))],
        [Text('File Organizer Section')],
        [Column(file_organizer_section, expand_x=True)],
        [Text('Network Tools Section')],
        [Column(network_section, expand_x=True)],
        [Text('System Information Section')],
        [Column(system_info_section, expand_x=True)],
        [Button('Exit')]
    ]

    # Create the window
    global window
    window = Window('Poseidon App', layout)

    # Event loop to capture input and trigger actions
    last_moved_files = []

    while True:
        event, values = window.read()

        # If user closes window or clicks Exit
        if event == WINDOW_CLOSED or event == 'Exit':
            break

        # Organize Files button
        if event == 'Organize Files':
            directory = values['directory_input']
            delete_empty_folders = values['delete_empty_folders']
            dry_run = values['dry_run']

            if directory:
                file_categories = {
                    'Images': ['.png', '.jpg', '.jpeg', '.gif'],
                    'Documents': ['.pdf', '.docx', '.txt', '.xls', '.xlsx'],
                    'Videos': ['.mp4', '.avi', '.mkv'],
                    'Audio': ['.mp3', '.wav', '.flac'],
                    'Compressed': ['.zip', '.rar', '.7z'],
                    'Executables': ['.exe', '.bat', '.sh']
                }
                last_moved_files = organize_files(directory, file_categories, delete_empty_folders, dry_run)
            else:
                notify_and_read("Please select a directory to organize.")

        # Undo Last Operation button
        if event == 'Undo Last Operation' and last_moved_files:
            undo_last_operation(last_moved_files)

        # Ping IP button
        if event == 'Ping IP':
            ip_address = values['ip_input']
            if ip_address:
                ping_network(ip_address)
            else:
                notify_and_read("Please enter a valid IP address.")

        # Scan Network button
        if event == 'Scan Network':
            ip_scan = values['network_input']
            if ip_scan:
                scan_network(ip_scan)
            else:
                notify_and_read("Please enter a valid network range.")

        # System Info button
        if event == 'Get System Info':
            get_system_info()

    # Close the window
    window.close()


# Run the GUI app
create_gui()
