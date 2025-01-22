import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QProgressBar,
    QPushButton, QFrame, QGridLayout, QSlider, QTextEdit, QTableWidget, QTableWidgetItem, QStackedWidget,
    QListWidget, QScrollArea, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QListWidget
)
from PyQt5.QtGui import QFont, QBrush, QColor, QConicalGradient, QPainter
from PyQt5.QtCore import Qt, QTimer, QPoint
from pages.settings_page import SettingsPage
from pages.reports_page import ReportsPage
from pages.logs_page import LogsPage
from pages.user_management_page import UserManagementPage
from db.alerts import network_alerts_db
from db.alerts import hvac_alerts_db
from db.alerts import ping_data_db
from db.cpu_usage import cpu_percent
from db.cpu_usage import total_memory
from db.cpu_usage import disk_used
from db.alerts import hvac_performance_db
from utils.alerts_removal import alert_removal

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pages = None
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
            QMainWindow { 
    background-color: #1b1b1f; /* A dark but softer black with a futuristic vibe */
}

QLabel { 
    color: #e0e0e0; /* Light grey for less strain on the eyes */
}

QPushButton { 
    background-color: #282a36; /* A dark, slightly bluish tone for buttons */
    color: #8be9fd; /* Soft cyan for text, matching the futuristic theme */
    border-radius: 5px; 
    padding: 10px; 
    border: 1px solid #6272a4; /* Subtle border for better visibility */
}

QPushButton:hover { 
    background-color: #44475a; /* Slightly brighter on hover for interactivity */
}

QFrame { 
    background-color: #21222c; /* A neutral dark tone for containers */
    border-radius: 10px; 
}

QProgressBar { 
    background-color: #282a36; /* Matches button color for consistency */
    color: #f8f8f2; /* Off-white text for clarity */
    border-radius: 5px; 
    text-align: center; 
}

QProgressBar::chunk { 
    background-color: #50fa7b; /* Futuristic green for progress */
}

QSlider::groove:horizontal { 
    background: #44475a; /* Dark groove for better contrast */
}

QSlider::handle:horizontal { 
    background: #bd93f9; /* Purple handle for a futuristic pop */
    border-radius: 5px; 
}

QTextEdit { 
    background-color: #282a36; /* Consistent dark background */
    color: #f8f8f2; /* Off-white text */
    border-radius: 5px; 
    padding: 5px; 
    border: 1px solid #6272a4; /* Subtle border for differentiation */
}

QLineEdit { 
    background-color: #282a36; 
    color: #f8f8f2; 
    border-radius: 5px; 
    padding: 5px; 
    border: 1px solid #6272a4; 
}

QTableWidget { 
    background-color: #21222c; 
    color: #f8f8f2; 
    border-radius: 5px; 
    padding: 5px; 
    gridline-color: #6272a4; /* Grid lines for clarity */
    selection-background-color: #44475a; /* Highlight selected rows */
}

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

    #Global Variables
    #toolTip

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

    @staticmethod
    def add_label(layout, text, color):
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
                background-color: #3498db;  /* Dark gray background */
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
                    padding: 10px;
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
        self.layout().setSpacing(20)

        # Add Widgets
        self.create_system_status()
        self.create_performance_metrics()
        self.create_lighting_dashboard()
        self.create_hvac_performance()
        # self.create_logs_section()

    def create_system_status(self):
        """System Status Section"""
        frame = self.create_frame("#34495e")
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
        metrics = [("CPU Usage", cpu_percent), ("Memory Usage", total_memory), ("Disk Usage", disk_used)]
        for metric, value in metrics:
            metric_label = QLabel(metric)
            metric_label.setFont(QFont("Arial", 14))
            metric_label.setStyleSheet("color: #ecf0f1;")

            progress_bar = QProgressBar()
            progress_bar.setRange(0,500)
            progress_bar.setValue(value)
            progress_bar.setStyleSheet("""
                QProgressBar { background-color: #2c3e50; border-radius: 5px; text-align: center; }
                QProgressBar::chunk { background-color: #3498db; }
            """)

            frame.layout().addWidget(metric_label)
            frame.layout().addWidget(progress_bar)

        self.layout().addWidget(frame, 1, 0)

    def create_lighting_dashboard(self):
        """Lighting Control Dashboard"""
        frame = self.create_frame("#34495e")

        # Add the title
        label = QLabel("Lighting Control Dashboard")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Grid layout for zones
        grid_layout = QGridLayout()
        zones = ["Living Room", "Kitchen", "Bedroom 1", "Bedroom 2", "Hallway"]
        lighting_data = {zone: {"status": "OFF", "brightness": 50} for zone in zones}

        for row, zone in enumerate(zones):
            # Zone name
            zone_label = QLabel(zone)
            zone_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")
            grid_layout.addWidget(zone_label, row, 0)

            # Toggle button
            toggle_button = QPushButton("OFF")
            toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c; 
                    color: #FFFFFF; 
                    border-radius: 5px; 
                    padding: 5px;
                }
                QPushButton:checked {
                    background-color: #2ecc71;
                }
            """)
            toggle_button.setCheckable(True)
            toggle_button.setCursor(Qt.PointingHandCursor)
            grid_layout.addWidget(toggle_button, row, 1)

            # Brightness slider
            brightness_slider = QSlider(Qt.Horizontal)
            brightness_slider.setValue(lighting_data[zone]["brightness"])
            brightness_slider.setStyleSheet("""
                QSlider::groove:horizontal { background: #444444; height: 6px; }
                QSlider::handle:horizontal { background: #00bcd4; width: 12px; margin: -5px 0; }
            """)
            grid_layout.addWidget(brightness_slider, row, 2)

            # Update toggle button and brightness on interaction
            def toggle_light(status_label, toggle_btn, zone_name):
                def inner():
                    if toggle_btn.isChecked():
                        toggle_btn.setText("ON")
                        lighting_data[zone_name]["status"] = "ON"
                    else:
                        toggle_btn.setText("OFF")
                        lighting_data[zone_name]["status"] = "OFF"

                return inner

            def adjust_brightness(bright_slider, zone_name):
                def inner(value):
                    lighting_data[zone_name]["brightness"] = value

                return inner

            toggle_button.clicked.connect(toggle_light(zone_label, toggle_button, zone))
            brightness_slider.valueChanged.connect(adjust_brightness(brightness_slider, zone))

        frame.layout().addLayout(grid_layout)
        self.layout().addWidget(frame, 1, 1)

    def create_hvac_performance(self):
        """HVAC Performance with Scrollable Progress Bars"""
        # Scroll Area Container
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: gray;")
        scroll_area.setWidgetResizable(True)

        # Frame inside the scroll area
        frame = QFrame()
        frame.setStyleSheet("background-color: #34495e; border-radius: 2px;")
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(10, 10, 10, 10)
        frame.layout().setSpacing(15)

        # Title
        label = QLabel("HVAC Performance")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Adding progress bars for each HVAC unit
        for data in hvac_performance_db:
            zone = data['equipment_name']
            performance = data['performance']
            zone_label = QLabel(f"{zone}: {performance}%")
            zone_label.setFont(QFont("Arial", 14))
            zone_label.setStyleSheet("color: #FFFFFF;")
            progress_bar = QProgressBar()
            progress_bar.setValue(performance)
            if performance > 90:
                color = "green"
            elif performance > 60:
                color = "yellow"
            else:
                color = "red"

            progress_bar.setStyleSheet(f"""
                 QProgressBar {{
                     color: #ecf0f1;
                     border-radius: 5px;
                     text-align: center;
                 }}
                 QProgressBar::chunk {{
                     background-color: {color};
                     border-radius: 5px;
                 }}
             """)
            frame.layout().addWidget(zone_label)
            frame.layout().addWidget(progress_bar)

        # Add frame to scroll area
        scroll_area.setWidget(frame)

        # Add scroll area to the main layout
        self.layout().addWidget(scroll_area, 2, 0, 1, 2)


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
        self.create_gauge_widget()
        self.create_network_alerts()
        self.create_alert_summary()


    def create_ping_monitor(self):
        """Ping Network Monitor Section with Scrollable Table"""
        # Create the main frame for the Ping Monitor
        frame = QFrame()
        frame.setStyleSheet("background-color: #34495e; border-radius: 10px;")
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(10, 10, 10, 10)
        frame.layout().setSpacing(10)

        # Add a label as the section title
        label = QLabel("🌐 Network Monitor")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # QTableWidget and data

        table = QTableWidget(len(ping_data_db), 3)
        table.setHorizontalHeaderLabels(["IP Address", "Ping", "Status"])
        table.horizontalHeader().setVisible(True)  # Ensure headers are visible
        table.verticalHeader().setVisible(False)  # Optional: Hide row headers
        table.setStyleSheet("""
            QTableWidget { background-color: #2c2c2c; color: #FFFFFF; }
            QHeaderView::section { background-color: #444444; color: #FFFFFF; padding: 4px; }
        """)
        for row, data in enumerate(ping_data_db):
            ip = data['IP']
            ping = data['ping']
            status = data['status']
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

        #  scroll area and frame
        scroll_area = QScrollArea()
        scroll_area.setWidget(frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #121212; border: none;")
        scroll_area.setMinimumHeight(100)  # Ensure it's large enough to display content

        # Add the scroll area to the main layout
        self.layout().addWidget(scroll_area)

        # scroll_area.setWidget(frame)
        # scroll_area.setWidget(frame)

    def create_hvac_sensor_status(self):
        """HVAC Sensor Status Section"""
        frame = self.create_frame("#34495e")
        frame.setLayout(QVBoxLayout())
        label = QLabel("🔥 HVAC Sensor Status")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # HVAC sensors
        table = QTableWidget(len(hvac_alerts_db), 3)
        table.setHorizontalHeaderLabels(["Zone", "Status", "Temperature"])
        table.horizontalHeader().setFixedHeight(60)
        table.horizontalHeader().setVisible(True)
        table.verticalHeader().setVisible(False)
        table.setStyleSheet("""
                    QTableWidget { background-color: #2c2c2c; color: #FFFFFF; border: none }
                    QHeaderView::section { background-color: #444444; color: #FFFFFF; padding: 4px; }
                """)
        table.setFixedHeight(200)
        for row, data in enumerate(hvac_alerts_db):
            zone = data['zone_id']
            status = data['severity']
            temp = str(data['temp'])

            table.setItem(row, 0, QTableWidgetItem(zone))
            status_item = QTableWidgetItem(status)
            if status == "Critical":
                status_item.setBackground(Qt.red)
            elif status == "Warning":
                status_item.setBackground(Qt.yellow)
            else:
                status_item.setBackground(Qt.green)
            table.setItem(row, 1, status_item)
            table.setItem(row, 2, QTableWidgetItem(temp + "°F"))

        frame.layout().addWidget(table)

        self.layout().addWidget(frame, 0, 1)

    def create_gauge_widget(self):
        """Improved Gauge Widget for Key Metric Visualization"""
        frame = self.create_frame("#34495e")

        # Title Label
        label = QLabel("📊 System Load")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Enhanced Gauge Widget
        class ImprovedGaugeWidget(QWidget):
            def __init__(self, parent=None, title="Metric", unit="%", min_val=0, max_val=100):
                super().__init__(parent)
                self.title = title
                self.unit = unit
                self.value = 50
                self.min_val = min_val
                self.max_val = max_val

                # Timer for Simulated Updates
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_value)
                self.timer.start(1000)

            def update_value(self):
                """Simulates dynamic gauge updates."""
                import random
                self.value = random.randint(self.min_val, self.max_val)
                self.update()

            def paintEvent(self, event):
                """Custom drawing for the gauge."""
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)

                rect = self.rect()
                size = min(rect.width(), rect.height())
                center = rect.center()
                radius = size // 2 - 10

                # Background Circle
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor("#2c3e50"))
                painter.drawEllipse(center, radius, radius)

                # Gradient Arc
                start_angle = 135 * 16  # Start angle (135°)
                span_angle = int((self.value / self.max_val) * 270) * 16  # Map value to angle
                gradient = QConicalGradient(center, -90)
                gradient.setColorAt(0.0, QColor("#27ae60"))  # Green for good performance
                gradient.setColorAt(1.0, QColor("#e74c3c"))  # Red for bad performance
                painter.setBrush(QBrush(gradient))
                painter.drawPie(
                    rect.center().x() - radius, rect.center().y() - radius,
                    radius * 2, radius * 2, start_angle, span_angle
                )

                # Inner Circle
                inner_radius = radius - 20
                painter.setBrush(QColor("#34495e"))  # Inner circle background
                painter.drawEllipse(center, inner_radius, inner_radius)

                # Draw Text (Value + Unit)
                painter.setPen(Qt.white)
                painter.setFont(QFont("Arial", 12, QFont.Bold))
                painter.drawText(
                    self.rect(),
                    Qt.AlignCenter,
                    f"{self.value} {self.unit}\n{self.title}"
                )

        # Add Gauge to Frame
        gauge = ImprovedGaugeWidget(title="System Load", unit="%", min_val=0, max_val=100)
        gauge.setFixedSize(220, 220)
        frame.layout().addWidget(gauge)


        # Add Frame to Main Layout
        self.layout().addWidget(frame, 1, 0)

    #db made for alert
    def create_network_alerts(self):
        """Display Ongoing Network Alerts"""
        frame = self.create_frame("#34495e")

        # Title Label
        label = QLabel("🚨 Network Alerts")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Network Alerts Text Box
        alerts = QListWidget()
        for item in network_alerts_db:
            alerts.addItem(
                f"🔴 Alert {item['id']} | {item['description']} | Acknowledge: | {item['acknowledge']}"
            )
        alerts.setStyleSheet(
            "background-color: #2c2c2c; color: #FFFFFF; border-radius: 5px; padding: 5px;"
        )
        frame.layout().addWidget(alerts)

        # Buttons (Reset and Acknowledge)
        reset_button = QPushButton("Reset")
        reset_button.setFont(QFont("Arial", 12))  # Smaller font
        reset_button.setFixedSize(120, 40)  # Smaller size
        reset_button.setCursor(Qt.PointingHandCursor)
        reset_button.setToolTip("Reset")
        reset_button.setStyleSheet(
            "background-color: #e53935; color: #FFFFFF; border-radius: 5px; padding: 5px;"
        )

        acknowledge_button = QPushButton("Acknowledge")
        acknowledge_button.setFont(QFont("Arial", 12))  # Smaller font
        acknowledge_button.setFixedSize(140, 40)  # Smaller size
        acknowledge_button.setCursor(Qt.PointingHandCursor)
        acknowledge_button.setToolTip("Acknowledge")
        acknowledge_button.setStyleSheet(
            "background-color: #8e24aa; color: #FFFFFF; border-radius: 5px; padding: 5px;"
        )
        acknowledge_button.clicked.connect(lambda: self.alert_removal(alerts))
        self.layout().update()


        # Horizontal Layout for Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(acknowledge_button)
        button_layout.setAlignment(Qt.AlignCenter)  # Center-align the buttons
        button_layout.setSpacing(20)  # Add some space between buttons

        # Add Button Layout Below Alerts
        frame.layout().addLayout(button_layout)

        # Add Frame to Main Layout
        self.layout().addWidget(frame, 1, 1)

    def create_alert_summary(self):
        """Summary of Alerts and Status"""
        frame = self.create_frame("#34495e")
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