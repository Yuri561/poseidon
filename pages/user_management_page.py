from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont


class UserManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Page Title
        title_label = QLabel("User Management")
        title_label.setFont(QFont("Arial", 24))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Add User Section
        add_user_frame = self.create_frame("Add User")
        username_input = QLineEdit()
        username_input.setPlaceholderText("Enter username...")
        add_user_button = QPushButton("Add User")
        add_user_button.setFont(QFont("Arial", 14))
        add_user_button.setStyleSheet("background-color: #4caf50; color: #FFFFFF; padding: 10px;")
        add_user_frame.layout().addWidget(username_input)
        add_user_frame.layout().addWidget(add_user_button)
        self.layout.addWidget(add_user_frame)

        # Delete User Section
        delete_user_frame = self.create_frame("Delete User")
        username_input_del = QLineEdit()
        username_input_del.setPlaceholderText("Enter username to delete...")
        delete_user_button = QPushButton("Delete User")
        delete_user_button.setFont(QFont("Arial", 14))
        delete_user_button.setStyleSheet("background-color: #f44336; color: #FFFFFF; padding: 10px;")
        delete_user_frame.layout().addWidget(username_input_del)
        delete_user_frame.layout().addWidget(delete_user_button)
        self.layout.addWidget(delete_user_frame)

    def create_frame(self, title):
        frame = QFrame()
        frame.setStyleSheet("background-color: #1e1e1e; border-radius: 10px; padding: 10px;")
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(QLabel(title, font=QFont("Arial", 16)))
        return frame
