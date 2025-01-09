from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QLineEdit, QPushButton, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Page Title
        title_label = QLabel("Settings")
        title_label.setFont(QFont("Arial", 24))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # System Settings
        settings_frame = self.create_frame("System Settings")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        settings_frame.layout().addWidget(QLabel("Adjust Threshold", font=QFont("Arial", 14)))
        settings_frame.layout().addWidget(slider)
        self.layout.addWidget(settings_frame)

        # Save Settings
        save_button = QPushButton("Save Settings")
        save_button.setFont(QFont("Arial", 16))
        save_button.setStyleSheet("background-color: #00bcd4; color: #FFFFFF; padding: 10px;")
        self.layout.addWidget(save_button)

    def create_frame(self, title):
        frame = QFrame()
        frame.setStyleSheet("background-color: #1e1e1e; border-radius: 10px; padding: 10px;")
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(QLabel(title, font=QFont("Arial", 16)))
        return frame
