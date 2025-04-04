from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer
from app.bot_selector import BotSelector

class LaunchScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberBot - Bienvenue")
        self.setFixedSize(800, 1000)
        self.setup_ui()

    def setup_ui(self):
        background = QPixmap("assets/images/logo.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background.scaled(self.size(), Qt.KeepAspectRatioByExpanding)))
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("")
        self.title_label.setFont(QFont("Orbitron", 24, QFont.Bold))
        self.title_label.setStyleSheet("color: #FFD700; text-shadow: 2px 2px 4px #000000;")
        self.title_label.setAlignment(Qt.AlignBottom)

        self.full_text = "Bienvenue dans CyberBot"
        self.current_index = 0
        self.animate_text()

        self.continue_btn = QPushButton("Continuer")
        self.continue_btn.setStyleSheet("padding: 10px 20px; font-size: 20px;")
        self.continue_btn.clicked.connect(self.open_bot_selector)

        layout.addWidget(self.title_label)
        layout.addSpacing(100)
        layout.addWidget(self.continue_btn)
        self.setLayout(layout)

    def animate_text(self):
        if self.current_index <= len(self.full_text):
            self.title_label.setText(self.full_text[:self.current_index])
            self.current_index += 1
            QTimer.singleShot(80, self.animate_text)

    def open_bot_selector(self):
        self.hide()
        self.selector = BotSelector()
        self.selector.show()
