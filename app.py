import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QProgressBar,
    QPushButton, QFrame, QGridLayout, QSlider, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QStackedWidget,
    QScrollBar, QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import datetime
from pages.settings_page import SettingsPage
from pages.reports_page import ReportsPage
from pages.logs_page import LogsPage
from pages.user_management_page import UserManagementPage

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dashboard = None
        self.alert_manager = None
        self.stacked_widget = None
        self.setWindowTitle("Prosyden")
        self.setMinimumSize(1900, 990)
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(20, 20, 20, 20)  # Add larger margins
        self.layout().setSpacing(30)

        # Apply Dark Mode
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QLabel { color: #FFFFFF; }
            QPushButton { background-color: #2c2c2c; color: #FFFFFF; border-radius: 5px; padding: 10px; }
            QPushButton:hover { background-color: #444444; }
            QFrame { background-color: #1e1e1e; border-radius: 10px; }
            QProgressBar { background-color: #2c2c2c; color: white; border-radius: 5px; text-align: center; }
            QProgressBar::chunk { background-color: #00bcd4; }
            QSlider::groove:horizontal { background: #444444; }
            QSlider::handle:horizontal { background: #00bcd4; border-radius: 5px; }
            QTextEdit { background-color: #2c2c2c; color: #FFFFFF; border-radius: 5px; padding: 5px; }
            QLineEdit { background-color: #2c2c2c; color: #FFFFFF; border-radius: 5px; padding: 5px; }
            QTableWidget { background-color: #2c2c2c; color: #FFFFFF; border-radius: 5px; padding: 5px; }
        """)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Top Section
        self.create_top_section()

        # Content Section
        self.create_content_section()

    def create_top_section(self):
        """Create the top section of the dashboard."""
        top_frame = QFrame()
        top_frame.setFixedHeight(100)

        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title_label = QLabel("Prosyden")
        title_label.setFont(QFont("Arial", 24))
        top_layout.addWidget(title_label)

        # System Labels
        self.add_label(top_layout, "Active Zone Alarms: 0", "#00bcd4")
        self.add_label(top_layout, "Active HVAC Alarms: 4", "#f44336")
        self.add_label(top_layout, "Network: Online", "#4caf50")
        self.add_label(top_layout, "Latency: 15ms", "#9c27b0")
        self.add_label(top_layout, "Energy Used: 250 kWh", "#ff9800")
        self.add_label(top_layout, "Critical Alerts: 2", "#f44336")

        self.main_layout.addWidget(top_frame)

    def add_label(self, layout, text, color):
        """Add a styled label to the layout."""
        label = QLabel(text)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet(f"background-color: {color}; color: #FFFFFF; border-radius: 5px; padding: 5px;")
        layout.addWidget(label)

    def create_content_section(self):
        """Create the content section with sidebar and dashboard."""
        content_layout = QHBoxLayout()

        # Sidebar
        self.create_sidebar(content_layout)

        # Stacked Widget for Pages
        self.stacked_widget = QStackedWidget()
        self.create_pages()
        content_layout.addWidget(self.stacked_widget)

        self.main_layout.addLayout(content_layout)

        # Dashboards
        self.dashboard = Dashboard()
        self.alert_manager = AlertManagerDashboard()
        # content_layout.addWidget(self.dashboard, stretch=2)
        content_layout.addWidget(self.alert_manager, stretch=2)

        self.main_layout.addLayout(content_layout)

    def create_sidebar(self, layout):
        """Create the sidebar for navigation."""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #00bcd4;  /* Dark gray background */
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
                padding: 10px;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)  # Add space for better appearance
        sidebar_layout.setSpacing(15)

        buttons = [
            ("Dashboard", lambda: self.show_page("dashboard")),
            ("Settings", lambda: self.show_page("settings")),
            ("Reports", lambda: self.show_page("reports")),
            ("Logs", lambda: self.show_page("logs")),
            ("User Management", lambda: self.show_page("user_management")),
        ]

        for btn_text, btn_action in buttons:
            button = QPushButton(btn_text)
            button.setFont(QFont("Arial", 14))
            button.setCursor(Qt.PointingHandCursor)  # Add a hover pointer for better UX
            button.clicked.connect(btn_action)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3c3c3c;  /* Slightly lighter gray */
                    color: #FFFFFF;  /* White text */
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #444444;  /* Slightly lighter hover effect */
                }
                QPushButton:pressed {
                    background-color: #555555;  /* Darker when pressed */
                }
            """)
            sidebar_layout.addWidget(button)

        # Add sidebar to the main layout
        layout.addWidget(sidebar)

    def create_pages(self):
        """Initialize all the pages and add them to the stacked widget."""
        self.pages = {
            "dashboard": Dashboard(),
            "settings": SettingsPage(),
            "reports": ReportsPage(),
            "logs": LogsPage(),
            "user_management": UserManagementPage(),
        }

        for page_name, page_widget in self.pages.items():
            self.stacked_widget.addWidget(page_widget)

    def show_page(self, page_name):
        """Switch to the specified page."""
        page = self.pages.get(page_name)
        if page:
            self.stacked_widget.setCurrentWidget(page)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(15, 15, 15, 15)
        self.layout().setSpacing(20)  # Improved spacing for readability

        # Add Widgets
        self.create_system_status()
        self.create_performance_metrics()
        self.create_network_table()
        self.create_hvac_performance()
        # self.create_logs_section()

    def create_system_status(self):
        """System Status Section"""
        frame = self.create_frame("#2c3e50")
        label = QLabel("System Status: All Systems Operational")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: #1abc9c;")  # Green text for operational status
        frame.layout().addWidget(label)

        # Additional details about system status
        details = QLabel("No alerts or critical issues detected. All services are running.")
        details.setFont(QFont("Arial", 12))
        details.setStyleSheet("color: #ecf0f1;")
        frame.layout().addWidget(details)

        self.layout().addWidget(frame, 0, 0, 1, 2)

    def create_performance_metrics(self):
        """Performance Metrics Section"""
        frame = self.create_frame("#34495e")
        label = QLabel("Metrics")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Progress Bars for CPU, Memory, and Disk Usage
        metrics = [("CPU Usage", 75), ("Memory Usage", 60), ("Disk Usage", 40)]
        for metric, value in metrics:
            metric_label = QLabel(metric)
            metric_label.setFont(QFont("Arial", 14))
            metric_label.setStyleSheet("color: #ecf0f1;")

            progress_bar = QProgressBar()
            progress_bar.setValue(value)
            progress_bar.setStyleSheet("""
                QProgressBar { background-color: #2c3e50; border-radius: 5px; text-align: center; }
                QProgressBar::chunk { background-color: #3498db; }
            """)

            frame.layout().addWidget(metric_label)
            frame.layout().addWidget(progress_bar)

        self.layout().addWidget(frame, 1, 0)

    def create_network_table(self):
        """Network Traffic Overview"""
        frame = self.create_frame("#8e44ad")
        label = QLabel("Network Traffic Overview")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Network Traffic Table
        table = QTableWidget(5, 3)
        table.setHorizontalHeaderLabels(["IP", "Stat", "Lat (ms)"])
        data = [
            ("192.168.1.1", "Online", "10ms"),
            ("192.168.1.2", "Online", "15ms"),
            ("192.168.1.3", "Offline", "N/A"),
            ("192.168.1.4", "Online", "20ms"),
            ("192.168.1.5", "Online", "5ms"),
        ]
        for row, (ip, status, latency) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(ip))
            status_item = QTableWidgetItem(status)
            if status == "Offline":
                status_item.setBackground(Qt.red)
            else:
                status_item.setBackground(Qt.green)
            table.setItem(row, 1, status_item)
            table.setItem(row, 2, QTableWidgetItem(latency))

        frame.layout().addWidget(table)
        self.layout().addWidget(frame, 1, 1)


    def create_hvac_performance(self):
        """HVAC Performance with Scrollable Progress Bars"""
        # Scroll Area Container
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: black;")
        scroll_area.setWidgetResizable(True)

        # Frame inside the scroll area
        frame = QFrame()
        frame.setStyleSheet("background-color: #16a085; border-radius: 2px;")
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(10, 10, 10, 10)
        frame.layout().setSpacing(15)

        # Title
        label = QLabel("HVAC Performance")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Example data for HVAC performance
        hvac_performance = [
            ("RTU-1", 90),
            ("RTU-2", 85),
            ("FCU-1", 78),
            ("FCU-2", 92),
            ("Tower", 88),
            ("RTU-3", 95),
            ("RTU-4", 65),
            ("FCU-3", 80),
            ("FCU-4", 75),
            ("Cooling Tower", 85),
        ]

        # Adding progress bars for each HVAC unit
        for zone, performance in hvac_performance:
            zone_label = QLabel(f"{zone}: {performance}%")
            zone_label.setFont(QFont("Arial", 14))
            zone_label.setStyleSheet("color: #FFFFFF;")
            progress_bar = QProgressBar()
            progress_bar.setValue(performance)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    background-color: #34495e;
                    color: #ecf0f1;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #e74c3c;
                    border-radius: 5px;
                }
            """)
            frame.layout().addWidget(zone_label)
            frame.layout().addWidget(progress_bar)

        # Add frame to scroll area
        scroll_area.setWidget(frame)

        # Add scroll area to the main layout
        self.layout().addWidget(scroll_area, 2, 0, 1, 2)

    # def create_logs_section(self):
    #     """System Logs Section"""
    #     frame = self.create_frame("#d35400")
    #     label = QLabel("System Logs")
    #     label.setFont(QFont("Arial", 16, QFont.Bold))
    #     label.setStyleSheet("color: #FFFFFF;")
    #     frame.layout().addWidget(label)
    #
    #     logs = QTextEdit()
    #     logs.setText("Log 1: System started\nLog 2: Network connected\nLog 3: User logged in")
    #     logs.setReadOnly(True)
    #     logs.setStyleSheet("background-color: #2c3e50; color: #ecf0f1; border-radius: 5px; padding: 5px;")
    #     frame.layout().addWidget(logs)
    #
    #     self.layout().addWidget(frame, 3, 0, 1, 2)

    def create_frame(self, color):
        """Reusable Frame with Custom Background Color"""
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {color}; border-radius: 10px; padding: 10px;")
        frame.setLayout(QVBoxLayout())
        return frame

class AlertManagerDashboard(QWidget):
    """Enhanced Alert Manager Dashboard Page"""
    def __init__(self):
        super().__init__()
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(10, 10, 10, 10)
        self.layout().setSpacing(10)

        # Add Widgets
        self.create_ping_monitor()
        self.create_hvac_sensor_status()
        self.create_alert_controls()
        self.create_network_alerts()
        self.create_alert_summary()

    def create_ping_monitor(self):
        """Ping Network Monitor Section"""
        frame = self.create_frame("#1e88e5")
        label = QLabel("🌐 Ping Network Monitor")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Simulate ping results
        ping_data = [
            ("192.168.1.1", "10ms", "Good"),
            ("192.168.1.2", "15ms", "Good"),
            ("192.168.1.3", "Timeout", "Critical"),
            ("192.168.1.4", "20ms", "Average"),
            ("192.168.1.5", "5ms", "Good"),
        ]
        table = QTableWidget(len(ping_data), 3)
        table.setHorizontalHeaderLabels(["IP Address", "Ping", "Status"])
        for row, (ip, ping, status) in enumerate(ping_data):
            table.setItem(row, 0, QTableWidgetItem(ip))
            table.setItem(row, 1, QTableWidgetItem(ping))
            status_item = QTableWidgetItem(status)
            if status == "Critical":
                status_item.setBackground(Qt.red)
            elif status == "Average":
                status_item.setBackground(Qt.yellow)
            else:
                status_item.setBackground(Qt.green)
            table.setItem(row, 2, status_item)

        frame.layout().addWidget(table)
        self.layout().addWidget(frame, 0, 0)

    def create_hvac_sensor_status(self):
        """HVAC Sensor Status Section"""
        frame = self.create_frame("#f4511e")
        label = QLabel("🔥 HVAC Sensor Status")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # HVAC sensors example
        sensor_data = [
            ("Zone 1", "Normal", "22°C"),
            ("Zone 2", "Warning", "27°C"),
            ("Zone 3", "Critical", "35°C"),
        ]
        table = QTableWidget(len(sensor_data), 3)
        table.setHorizontalHeaderLabels(["Zone", "Status", "Temperature"])
        for row, (zone, status, temp) in enumerate(sensor_data):
            table.setItem(row, 0, QTableWidgetItem(zone))
            status_item = QTableWidgetItem(status)
            if status == "Critical":
                status_item.setBackground(Qt.red)
            elif status == "Warning":
                status_item.setBackground(Qt.yellow)
            else:
                status_item.setBackground(Qt.green)
            table.setItem(row, 1, status_item)
            table.setItem(row, 2, QTableWidgetItem(temp))

        frame.layout().addWidget(table)
        self.layout().addWidget(frame, 0, 1)

    def create_alert_controls(self):
        """Alert Management Controls"""
        frame = self.create_frame("#43a047")
        label = QLabel("⚠️ Manage Alerts")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Alert actions with sliders and toggles
        reset_button = QPushButton("Reset Alarms")
        reset_button.setFont(QFont("Arial", 14))
        reset_button.setStyleSheet("background-color: #e53935; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        acknowledge_button = QPushButton("Acknowledge Alerts")
        acknowledge_button.setFont(QFont("Arial", 14))
        acknowledge_button.setStyleSheet("background-color: #8e24aa; color: #FFFFFF; border-radius: 5px; padding: 10px;")

        slider_label = QLabel("Alert Sensitivity:")
        slider_label.setFont(QFont("Arial", 12))
        slider_label.setStyleSheet("color: #FFFFFF;")

        sensitivity_slider = QSlider(Qt.Horizontal)
        sensitivity_slider.setMinimum(0)
        sensitivity_slider.setMaximum(100)
        sensitivity_slider.setValue(50)
        sensitivity_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #444444; }
            QSlider::handle:horizontal { background: #00bcd4; border-radius: 5px; }
        """)

        frame.layout().addWidget(reset_button)
        frame.layout().addWidget(acknowledge_button)
        frame.layout().addWidget(slider_label)
        frame.layout().addWidget(sensitivity_slider)

        self.layout().addWidget(frame, 1, 0)

    def create_network_alerts(self):
        """Display Ongoing Network Alerts"""
        frame = self.create_frame("#ff9800")
        label = QLabel("🚨 Network Alerts")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Example alerts
        alerts = QTextEdit()
        alerts.setText(
            "🔴 Alert 1: High latency detected on 192.168.1.3\n"
            "🔴 Alert 2: Packet loss on 192.168.1.4\n"
            "🟠 Alert 3: Network timeout for 192.168.1.5"
        )
        alerts.setReadOnly(True)
        alerts.setStyleSheet("background-color: #2c2c2c; color: #FFFFFF; border-radius: 5px; padding: 5px;")
        frame.layout().addWidget(alerts)

        self.layout().addWidget(frame, 1, 1)

    def create_alert_summary(self):
        """Summary of Alerts and Status"""
        frame = self.create_frame("#3949ab")
        label = QLabel("📊 Summary")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        summary_text = QTextEdit()
        summary_text.setText(
            "🔹 Total Alerts: 10\n"
            "🔸 Resolved Alerts: 7\n"
            "🔴 Critical Alerts: 3"
        )
        summary_text.setReadOnly(True)
        summary_text.setStyleSheet("background-color: #2c2c2c; color: #FFFFFF; border-radius: 5px; padding: 5px;")

        frame.layout().addWidget(summary_text)
        self.layout().addWidget(frame, 2, 0, 1, 2)

    def create_frame(self, color):
        """Reusable Frame Creation with Custom Background Color"""
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {color}; border-radius: 10px; padding: 10px;")
        frame.setLayout(QVBoxLayout())
        return frame



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
