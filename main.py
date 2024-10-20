import os
import shutil
import pyttsx3
import subprocess
from win11toast import toast  # For Windows 11 notifications

# Initialize text-to-speech
engine = pyttsx3.init()

#checking for voices in the system

def get_voices():
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"ID: {voice.id}")
        print(f"Name: {voice.name}")

# File Organizer Function
def organize_files(directory):
    if not os.path.exists(directory):
        notify_and_read(f"Directory {directory} does not exist.")
        return

    file_types = {
        'Images': ['.png', '.jpg', '.jpeg', '.gif'],
        'Documents': ['.pdf', '.docx', '.txt', '.xls'],
        'Videos': ['.mp4', '.avi'],
        'Audio': ['.mp3', '.wav'],
    }

    for folder, extensions in file_types.items():
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1]
                if file_ext in extensions:
                    shutil.move(file_path, folder_path)
                    notify_and_read(f"Moved {filename} to {folder}")

# Notification Reader Function
def notify_and_read(message):
    # Use win11toast to show notification
    toast("Poseidon Notification", message, duration="short")
    # Text-to-speech for the message
    engine.say(message)
    engine.runAndWait()

# App Launcher Function
def launch_app(app_name):
    apps = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'browser': 'chrome.exe',
        # Add more apps here as needed
    }

    # Launch the selected application if it exists, otherwise notify the user
    if app_name in apps:
        subprocess.Popen(apps[app_name])
        notify_and_read(f"Opening {app_name}")
    else:
        notify_and_read(f"Application {app_name} not found.")

# Ping Network Function
def ping_network(ip_address):
    response = os.system(f"ping {ip_address}")
    if response == 0:
        notify_and_read(f"Successfully pinged {ip_address}")
    else:
        notify_and_read(f"Failed to ping {ip_address}. Check the IP address and try again.")

# Main Menu Function
def main_menu():
    while True:
        print("\n==== Welcome to Poseidon ====")
        print("Please choose an option:")
        print("1. Organize Files")
        print("2. Launch Application")
        print("3. Ping a Network IP")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            directory = input("Enter the directory to organize: ")
            organize_files(directory)
        elif choice == '2':
            app_name = input("Enter the name of the application to launch (e.g., notepad, calculator): ")
            launch_app(app_name)
        elif choice == '3':
            ip_address = input("Enter the IP address to ping: ")
            ping_network(ip_address)
        elif choice == '4':
            notify_and_read("Goodbye!")
            break
        else:
            notify_and_read("Invalid choice. Please choose 1, 2, 3, or 4.")

# Run the Poseidon Program
if __name__ == "__main__":
    main_menu()
