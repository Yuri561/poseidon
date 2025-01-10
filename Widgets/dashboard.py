from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QProgressBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Dashboard(QWidget):
    def __init__(self) -> object:
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
        label = QLabel("Net Traffic Overview")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: #FFFFFF;")
        frame.layout().addWidget(label)

        # Network Traffic Table
        table = QTableWidget(5, 3)
        table.setHorizontalHeaderLabels(["IP", "Stat", "Lat (ms)"])
        table.horizontalHeader().setVisible(True)
        table.horizontalHeader().setFixedHeight(65)
        table.verticalHeader().setVisible(False)
        table.setStyleSheet("""
                   QTableWidget {color: #FFFFFF; }
                   QHeaderView::section { background-color: #444444; color: #FFFFFF; padding: 4px; }
               """)
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


    def create_frame(self, color):
        """Reusable Frame with Custom Background Color"""
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {color}; border-radius: 10px; padding: 10px;")
        frame.setLayout(QVBoxLayout())
        return frame