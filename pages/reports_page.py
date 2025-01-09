from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QFrame
from PyQt5.QtGui import QFont


class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Page Title
        title_label = QLabel("Reports")
        title_label.setFont(QFont("Arial", 24))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Reports Viewer
        reports_frame = self.create_frame("Generated Reports")
        reports_viewer = QTextEdit()
        reports_viewer.setText("Report 1: System Overview\nReport 2: Performance Metrics\nReport 3: Alerts Summary")
        reports_viewer.setReadOnly(True)
        reports_frame.layout().addWidget(reports_viewer)
        self.layout.addWidget(reports_frame)

    def create_frame(self, title):
        frame = QFrame()
        frame.setStyleSheet("background-color: #1e1e1e; border-radius: 10px; padding: 10px;")
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(QLabel(title, font=QFont("Arial", 16)))
        return frame
