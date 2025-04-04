from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
import os

class ChatHistoryViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historique des Chats")
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: black; color: white;")
        self.setup_ui()
        self.load_history_list()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        title = QLabel("📃 Historique des discussions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #00ffff; margin-bottom: 10px;")
        self.layout.addWidget(title)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet("background-color: #111; color: white; font-size: 14px;")
        self.file_list.itemClicked.connect(self.display_file_content)
        self.layout.addWidget(self.file_list)

        self.content_display = QTextEdit()
        self.content_display.setReadOnly(True)
        self.content_display.setStyleSheet("background-color: #1a1a1a; padding: 10px; border: 1px solid #444; font-size: 14px;")
        self.layout.addWidget(self.content_display)

    def load_history_list(self):
        os.makedirs("chat_logs", exist_ok=True)
        for filename in sorted(os.listdir("chat_logs"), reverse=True):
            if filename.endswith(".txt"):
                item = QListWidgetItem(filename)
                self.file_list.addItem(item)

    def display_file_content(self, item):
        path = os.path.join("chat_logs", item.text())
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            self.content_display.setText(content)
