from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QFrame
from PyQt5.QtGui import QFont


class LogsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Page Title
        title_label = QLabel("Logs")
        title_label.setFont(QFont("Arial", 24))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Logs Viewer
        logs_frame = self.create_frame("System Logs")
        logs_viewer = QTextEdit()
        logs_viewer.setText("Log 1: System initialized\nLog 2: Network connected\nLog 3: User login detected")
        logs_viewer.setReadOnly(True)
        logs_frame.layout().addWidget(logs_viewer)
        self.layout.addWidget(logs_frame)

    def create_frame(self, title):
        frame = QFrame()
        frame.setStyleSheet("background-color: #1e1e1e; border-radius: 10px; padding: 10px;")
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(QLabel(title, font=QFont("Arial", 16)))
        return frame
