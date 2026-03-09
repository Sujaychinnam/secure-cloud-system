from PySide6.QtWidgets import *

class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Secure Cloud Storage")

        layout = QVBoxLayout()

        upload = QPushButton("Upload File")
        share = QPushButton("Share File")
        download = QPushButton("Download File")

        layout.addWidget(upload)
        layout.addWidget(share)
        layout.addWidget(download)

        self.setLayout(layout)


app = QApplication([])
window = Dashboard()
window.show()
app.exec()