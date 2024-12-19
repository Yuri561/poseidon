import socket
from threading import Thread
import customtkinter as ctk

class NetworkScannerTab:
    def __init__(self, parent_tab):
        self.parent_tab = parent_tab
        self.build_network_scanner_tab()

    def build_network_scanner_tab(self):
        """Build the Network Scanner tab."""
        ctk.CTkLabel(self.parent_tab, text="Network Scanner", font=("Arial", 16)).pack(pady=10)

        # IP Range Input
        ctk.CTkLabel(self.parent_tab, text="Start IP:").pack(pady=5)
        self.start_ip_entry = ctk.CTkEntry(self.parent_tab, placeholder_text="192.168.1.1")
        self.start_ip_entry.pack(pady=5)

        ctk.CTkLabel(self.parent_tab, text="End IP:").pack(pady=5)
        self.end_ip_entry = ctk.CTkEntry(self.parent_tab, placeholder_text="192.168.1.255")
        self.end_ip_entry.pack(pady=5)

        # Scan Button
        self.scan_button = ctk.CTkButton(
            self.parent_tab, text="Start Scan", command=self.start_scan
        )
        self.scan_button.pack(pady=10)

        # Results Display
        self.results_label = ctk.CTkLabel(self.parent_tab, text="Active IPs:")
        self.results_label.pack(pady=5)
        self.results_listbox = ctk.CTkTextbox(self.parent_tab, height=15, width=60)
        self.results_listbox.pack(pady=5)

    def start_scan(self):
        """Start the network scanning process."""
        start_ip = self.start_ip_entry.get()
        end_ip = self.end_ip_entry.get()
        self.results_listbox.delete("0.0", "end")

        if not self.validate_ips(start_ip, end_ip):
            self.results_listbox.insert("0.0", "Invalid IP range. Ensure they are in the same subnet.\n")
            return

        self.results_listbox.insert("0.0", "Scanning...\n")

        # Start scanning in a separate thread to keep the GUI responsive
        scan_thread = Thread(target=self.scan_ip_range, args=(start_ip, end_ip))
        scan_thread.start()

    def validate_ips(self, start_ip, end_ip):
        """Validate the start and end IPs."""
        try:
            start_parts = list(map(int, start_ip.split('.')))
            end_parts = list(map(int, end_ip.split('.')))
            if len(start_parts) != 4 or len(end_parts) != 4:
                return False
            if start_parts[:-1] != end_parts[:-1]:
                return False
            if not (0 <= start_parts[-1] <= 255 and 0 <= end_parts[-1] <= 255):
                return False
            if start_parts[-1] > end_parts[-1]:
                return False
            return True
        except ValueError:
            return False

    def scan_ip_range(self, start_ip, end_ip):
        """Scan a range of IPs and display active ones."""
        active_ips = []
        start_last_octet = int(start_ip.split('.')[-1])
        end_last_octet = int(end_ip.split('.')[-1])
        base_ip = '.'.join(start_ip.split('.')[:-1])

        for i in range(start_last_octet, end_last_octet + 1):
            ip = f"{base_ip}.{i}"
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.5)
                    sock.connect((ip, 80))
                    active_ips.append(ip)

                # Update results in the GUI asynchronously
                self.results_listbox.insert("end", f"Active: {ip}\n")
            except (socket.timeout, OSError):
                pass

        if not active_ips:
            self.results_listbox.insert("end", "No active IPs found.\n")
