import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import socket
import psutil
from threading import Thread
from time import sleep

class PoseidonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Poseidon App")
        self.geometry("800x600")

        # Tab creation
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        # Add tabs
        self.network_tab = self.tabview.add("Network Scanner")
        self.system_tab = self.tabview.add("System Monitor")

        # Build tabs
        self.build_network_scanner_tab()
        self.build_system_monitor_tab()

    def build_network_scanner_tab(self):
        """Build the Network Scanner tab."""
        # IP Range Input
        ctk.CTkLabel(self.network_tab, text="Start IP:").pack(pady=5)
        self.start_ip_entry = ctk.CTkEntry(self.network_tab, placeholder_text="192.168.1.1")
        self.start_ip_entry.pack(pady=5)

        ctk.CTkLabel(self.network_tab, text="End IP:").pack(pady=5)
        self.end_ip_entry = ctk.CTkEntry(self.network_tab, placeholder_text="192.168.1.255")
        self.end_ip_entry.pack(pady=5)

        # Scan Button
        self.scan_button = ctk.CTkButton(
            self.network_tab, text="Start Scan", command=self.start_scan
        )
        self.scan_button.pack(pady=10)

        # Results Display
        self.results_label = ctk.CTkLabel(self.network_tab, text="Active IPs:")
        self.results_label.pack(pady=5)
        self.results_box = ctk.CTkTextbox(self.network_tab, height=30, width=100)
        self.results_box.pack(pady=5)

    def start_scan(self):
        """Start the network scanning process."""
        start_ip = self.start_ip_entry.get()
        end_ip = self.end_ip_entry.get()
        self.results_box.delete("0.0", "end")
        self.results_box.insert("0.0", "Scanning...\n")

        # Start scanning in a separate thread to keep the GUI responsive
        scan_thread = Thread(target=self.scan_ip_range, args=(start_ip, end_ip))
        scan_thread.start()

    def scan_ip_range(self, start_ip, end_ip):
        """Scan a range of IPs and display active ones."""
        active_ips = []
        try:
            start_last_octet = int(start_ip.split('.')[-1])
            end_last_octet = int(end_ip.split('.')[-1])
            base_ip = '.'.join(start_ip.split('.')[:-1])

            for i in range(start_last_octet, end_last_octet + 1):
                ip = f"{base_ip}.{i}"
                try:
                    socket.create_connection((ip, 80), timeout=0.5)
                    active_ips.append(ip)
                except:
                    pass

            self.results_box.delete("0.0", "end")
            if active_ips:
                self.results_box.insert("0.0", "\n".join(active_ips))
            else:
                self.results_box.insert("0.0", "No active IPs found.")
        except Exception as e:
            self.results_box.insert("0.0", f"Error: {str(e)}")

    def build_system_monitor_tab(self):
        """Build the System Monitor tab."""
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("CPU Usage")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Usage (%)")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.system_tab)
        self.canvas.get_tk_widget().pack()

        # Start real-time graph update
        self.update_graph_thread = Thread(target=self.update_system_graph, daemon=True)
        self.update_graph_thread.start()

    def update_system_graph(self):
        """Update the CPU usage graph in real-time."""
        cpu_data = []
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_data.append(cpu_usage)
            if len(cpu_data) > 20:  # Limit to the last 20 data points
                cpu_data.pop(0)

            self.ax.clear()
            self.ax.plot(cpu_data, marker='o', color='blue')
            self.ax.set_title("CPU Usage")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Usage (%)")
            self.canvas.draw()

if __name__ == "__main__":
    app = PoseidonApp()
    app.mainloop()
