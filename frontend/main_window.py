import sys
import os
import datetime

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QTextEdit, QPushButton, QInputDialog,
    QLabel, QProgressBar
)

from PySide6.QtGui import QPixmap

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.crypto_engine import encrypt_file, decrypt_file
from backend.ecc_engine import encrypt_key, decrypt_key
from backend.blockchain import Blockchain
from backend.user_manager import UserManager
from backend.key_loader import load_private_key
from backend.cloud_storage import upload_file, download_file
from backend.file_sync import FileSync

from frontend.blockchain_viewer import show_blockchain


# ==========================================
# Drag Drop File Table
# ==========================================

class FileTable(QTableWidget):

    def __init__(self, logger, blockchain, parent):

        super().__init__()

        self.logger = logger
        self.blockchain = blockchain
        self.parent_window = parent

        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["File Name", "Size", "Date"])

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()

            for url in event.mimeData().urls():

                file_path = url.toLocalFile()

                self.logger(f"File dropped: {file_path}")

                self.process_file(file_path)

    # ==========================================
    # Process File
    # ==========================================

    def process_file(self, path):

        name = os.path.basename(path)

        size = os.path.getsize(path) / 1024
        size = f"{round(size,2)} KB"

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        row = self.rowCount()

        self.insertRow(row)

        self.setItem(row,0,QTableWidgetItem(name))
        self.setItem(row,1,QTableWidgetItem(size))
        self.setItem(row,2,QTableWidgetItem(date))

        self.logger("File added to table")

        self.parent_window.progress.setValue(20)

        # AES encryption
        key, encrypted_file = encrypt_file(path)

        self.logger("AES encryption completed")

        self.parent_window.progress.setValue(40)

        # upload encrypted file
        cloud_name = upload_file(encrypted_file)

        if cloud_name:
            self.logger(f"Uploaded to cloud: {cloud_name}")
        else:
            self.logger("Cloud upload failed")

        self.parent_window.progress.setValue(60)

        manager = UserManager()

        receiver = self.parent_window.selected_receiver

        public_key = manager.get_public_key(receiver)

        cipher_key, point = encrypt_key(key, public_key)

        self.logger("AES key encrypted using receiver public key")

        self.parent_window.progress.setValue(80)

        # blockchain entry
        self.blockchain.add_block(
            cloud_name,
            cipher_key,
            self.parent_window.username,
            receiver
        )

        self.logger("Block added to blockchain")

        self.parent_window.progress.setValue(100)

        # preview file
        self.parent_window.preview_file(path)


# ==========================================
# Main Window
# ==========================================

class MainWindow(QMainWindow):

    def __init__(self, username):

        super().__init__()

        self.username = username
        self.selected_receiver = username

        self.blockchain = Blockchain()

        # start realtime sync
        self.sync = FileSync(self.sync_event)
        self.sync.start()

        self.setWindowTitle("Secure Cloud Storage")
        self.resize(1000,600)

        main_widget = QWidget()

        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        # sidebar
        sidebar = QVBoxLayout()

        share_btn = QPushButton("Share File")
        share_btn.clicked.connect(self.share_file)

        unlock_btn = QPushButton("Unlock File")
        unlock_btn.clicked.connect(self.unlock_file)

        blockchain_btn = QPushButton("View Blockchain")
        blockchain_btn.clicked.connect(self.show_chain)

        sidebar.addWidget(share_btn)
        sidebar.addWidget(unlock_btn)
        sidebar.addWidget(blockchain_btn)

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)

        # main file table
        self.file_table = FileTable(self.log,self.blockchain,self)

        # log panel
        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setMaximumHeight(150)

        # upload progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)

        # shared files dashboard
        self.shared_table = QTableWidget()

        self.shared_table.setColumnCount(2)

        self.shared_table.setHorizontalHeaderLabels(
            ["Shared File","Owner"]
        )

        top_layout.addWidget(sidebar_widget,1)
        top_layout.addWidget(self.file_table,4)

        main_layout.addLayout(top_layout)

        main_layout.addWidget(self.progress)

        main_layout.addWidget(self.shared_table)

        main_layout.addWidget(self.log_panel)

        main_widget.setLayout(main_layout)

        # load shared files
        self.load_shared_files()

    # ==========================================
    # Logger
    # ==========================================

    def log(self,message):

        self.log_panel.append(message)

    # ==========================================
    # File Preview
    # ==========================================

    def preview_file(self,path):

        if path.endswith(".png") or path.endswith(".jpg"):

            preview = QLabel()

            pixmap = QPixmap(path)

            preview.setPixmap(pixmap.scaled(300,300))

            preview.show()

        elif path.endswith(".txt"):

            with open(path) as f:
                text = f.read()

            self.log(text)

    # ==========================================
    # Share File
    # ==========================================

    def share_file(self):

        manager = UserManager()

        users = list(manager.load_users().keys())

        receiver, ok = QInputDialog.getItem(
            self,
            "Share File",
            "Select Receiver:",
            users,
            0,
            False
        )

        if ok:

            self.selected_receiver = receiver

            self.log(f"File will be shared with {receiver}")

    # ==========================================
    # Load Shared Files
    # ==========================================

    def load_shared_files(self):

        for block in self.blockchain.chain:

            if block.get("receiver") == self.username:

                file_name = block.get("file_name")

                if file_name and file_name != "genesis":

                    row = self.shared_table.rowCount()

                    self.shared_table.insertRow(row)

                    self.shared_table.setItem(
                        row,0,
                        QTableWidgetItem(file_name)
                    )

                    self.shared_table.setItem(
                        row,1,
                        QTableWidgetItem(block["owner"])
                    )

    # ==========================================
    # Unlock File (permission check)
    # ==========================================

    def unlock_file(self):

        for block in self.blockchain.chain:

            permissions = block.get("permissions",[])

            if self.username not in permissions:
                continue

            cipher_key = bytes.fromhex(block["encrypted_key"])

            private_key = load_private_key(self.username)

            point = None

            aes_key = decrypt_key(cipher_key,private_key,point)

            cloud_file = download_file(block["file_name"])

            decrypted = decrypt_file(cloud_file,aes_key)

            self.log(f"File decrypted: {decrypted}")

    # ==========================================
    # Blockchain Visualization
    # ==========================================

    def show_chain(self):

        show_blockchain(self.blockchain.chain)

    # ==========================================
    # Real-time Sync Event
    # ==========================================

    def sync_event(self,file_name):

        self.log(f"New cloud file detected: {file_name}")