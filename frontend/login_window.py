from PySide6.QtWidgets import *
from backend.user_manager import UserManager


class LoginWindow(QWidget):

    def __init__(self, success_callback):

        super().__init__()

        self.manager = UserManager()

        self.success_callback = success_callback

        self.setWindowTitle("Secure Cloud Login")

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Password")

        login_btn = QPushButton("Login")
        register_btn = QPushButton("Register")

        login_btn.clicked.connect(self.login)
        register_btn.clicked.connect(self.register)

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)

        layout.addWidget(login_btn)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def login(self):

        user = self.username.text()
        pwd = self.password.text()

        if self.manager.login(user, pwd):

            QMessageBox.information(self, "Success", "Login successful")

            self.success_callback(user)

            self.close()

        else:

            QMessageBox.warning(self, "Error", "Invalid login")

    def register(self):

        user = self.username.text()
        pwd = self.password.text()

        if self.manager.register(user, pwd):

            QMessageBox.information(self, "Success", "User registered")

        else:

            QMessageBox.warning(self, "Error", "User already exists")