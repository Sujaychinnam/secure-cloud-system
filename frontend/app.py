import sys
import qdarkstyle

from PySide6.QtWidgets import QApplication

from .main_window import MainWindow
from .login_window import LoginWindow


app = QApplication(sys.argv)

# Apply modern dark theme
app.setStyleSheet(qdarkstyle.load_stylesheet())


def open_dashboard(username):

    window = MainWindow(username)

    window.show()


login = LoginWindow(open_dashboard)

login.show()

sys.exit(app.exec())