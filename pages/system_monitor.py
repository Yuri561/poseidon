from threading import Thread
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil

class SystemMonitorTab:
    def __init__(self, parent_tab):
        self.parent_tab = parent_tab
        self.build_system_monitor_tab()

    def build_system_monitor_tab(self):
        """Build the System Monitor tab."""
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("CPU Usage")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Usage (%)")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent_tab)
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
            self.ax.plot(cpu_data, marker="o", color="blue")
            self.ax.set_title("CPU Usage")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Usage (%)")
            self.canvas.draw()
