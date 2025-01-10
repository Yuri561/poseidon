from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QScrollArea, \
    QPushButton, QSlider, QFrame, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


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
        """Ping Network Monitor Section with Scrollable Table"""
        # Create the main frame for the Ping Monitor
        frame = QFrame()
        frame.setStyleSheet("background-color: #1e88e5; border-radius: 10px;")
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(10, 10, 10, 10)
        frame.layout().setSpacing(10)

        # Add a label as the section title
        label = QLabel("🌐 Ping Network Monitor")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Create the QTableWidget and populate it with data
        ping_data = [
            ("192.168.1.1", "10ms", "Good"),
            ("192.168.1.2", "15ms", "Good"),
            ("192.168.1.3", "Timeout", "Critical"),
            ("192.168.1.4", "20ms", "Average"),
            ("192.168.1.5", "5ms", "Good"),
        ]

        table = QTableWidget(len(ping_data), 3)
        table.setHorizontalHeaderLabels(["IP Address", "Ping", "Status"])
        table.horizontalHeader().setVisible(True)  # Ensure headers are visible
        table.verticalHeader().setVisible(False)  # Optional: Hide row headers
        table.setStyleSheet("""
            QTableWidget { background-color: #2c2c2c; color: #FFFFFF; }
            QHeaderView::section { background-color: #444444; color: #FFFFFF; padding: 4px; }
        """)
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

        # Create a scroll area and add the frame to it
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
        table.horizontalHeader().setFixedHeight(60)
        table.horizontalHeader().setVisible(True)
        table.verticalHeader().setVisible(False)  # Optional: Hide row headers
        table.setStyleSheet("""
                    QTableWidget { background-color: #2c2c2c; color: #FFFFFF; border: none }
                    QHeaderView::section { background-color: #444444; color: #FFFFFF; padding: 4px; }
                """)
        table.setFixedHeight(200)
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
        reset_button.setCursor(Qt.PointingHandCursor)
        reset_button.setToolTip('Reset')
        reset_button.setStyleSheet("background-color: #e53935; color: #FFFFFF; border-radius: 5px; padding: 10px;")

        acknowledge_button = QPushButton("Acknowledge Alerts")
        acknowledge_button.setFont(QFont("Arial", 14))
        acknowledge_button.setCursor(Qt.PointingHandCursor)
        acknowledge_button.setToolTip("Acknowledge")
        acknowledge_button.setStyleSheet("""background-color: #8e24aa; color: #FFFFFF; border-radius: 5px; padding: 10px;
        """ )

        slider_label = QLabel("Alert Sensitivity:")
        slider_label.setFont(QFont("Arial", 12))
        slider_label.setStyleSheet("color: #FFFFFF;")

        sensitivity_slider = QSlider(Qt.Horizontal)
        sensitivity_slider.setMinimum(0)
        sensitivity_slider.setMaximum(100)
        sensitivity_slider.setValue(50)
        sensitivity_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #444444; }
            QSlider::handle:horizontal { background: #00bcd4; border-radius: 5px; padding: 8px; }
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

        # neetwork alerts
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
