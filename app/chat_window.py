from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMenu, QAction
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import subprocess
import os
import datetime
import shlex

class ChatWindow(QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.setWindowTitle(f"Chat de {bot['name']}")
        self.setFixedSize(800, 1000)
        self.setStyleSheet("background-color: white; color: #1a1a1a;")

        self.language = "fr"
        self.persona = self.get_persona(bot['name'])
        self.log = []
        self.setup_ui()
        self.send_welcome_message()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("⬅")
        self.back_btn.setFixedSize(40, 30)
        self.back_btn.setStyleSheet("background-color: #0078D7; color: white; border: none; border-radius: 5px;")
        self.back_btn.clicked.connect(self.return_to_selector)

        self.menu_btn = QPushButton("🌐 FR/EN")
        self.menu_btn.setFixedSize(90, 30)
        self.menu_btn.setStyleSheet("background-color: #0078D7; color: white; border: none; border-radius: 5px;")
        self.menu_btn.setMenu(self.build_menu())

        top_bar.addWidget(self.back_btn)
        top_bar.addStretch()
        top_bar.addWidget(self.menu_btn)
        self.layout.addLayout(top_bar)

        self.title = QLabel(f"💬 Chat de {self.bot['name']}")
        self.title.setFont(QFont("Arial", 22, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #0078D7; padding: 10px; background-color: #E6F0FA; border-radius: 6px;")
        self.layout.addWidget(self.title)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial", 14))
        self.chat_display.setStyleSheet("padding: 10px; background-color: #f9f9f9; border: 1px solid #ccc; border-radius: 10px;")
        self.layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Écris ton message ici...")
        self.user_input.setFont(QFont("Arial", 14))
        self.user_input.returnPressed.connect(self.handle_send)
        self.user_input.setStyleSheet("padding: 10px; border-radius: 8px; border: 1px solid #0078D7; background-color: #ffffff; color: #1a1a1a;")

        self.send_btn = QPushButton("Envoyer")
        self.send_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.send_btn.setStyleSheet("background-color: #0078D7; color: white; border: none; border-radius: 8px; padding: 8px;")
        self.send_btn.clicked.connect(self.handle_send)

        self.restart_btn = QPushButton("Nouvelle conversation")
        self.restart_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.restart_btn.setStyleSheet("background-color: #cccccc; color: black; border-radius: 8px; padding: 6px;")
        self.restart_btn.clicked.connect(self.restart_conversation)

        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_btn)

        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.restart_btn)

    def build_menu(self):
        menu = QMenu()
        action_history = QAction("📁 Liste des discussions", self)
        action_history.triggered.connect(self.open_chat_history)

        action_fr = QAction("🇫🇷 Français", self)
        action_fr.triggered.connect(lambda: self.set_language("fr"))

        action_en = QAction("🇬🇧 Anglais", self)
        action_en.triggered.connect(lambda: self.set_language("en"))

        menu.addAction(action_history)
        menu.addSeparator()
        menu.addAction(action_fr)
        menu.addAction(action_en)
        return menu

    def set_language(self, lang):
        self.language = lang
        self.add_bot_message(f"Langue changée en {'Français' if lang == 'fr' else 'Anglais'}.")

    def open_chat_history(self):
        os.makedirs("chat_logs", exist_ok=True)
        os.startfile("chat_logs")

    def return_to_selector(self):
        self.close()
        from app.bot_selector import BotSelector
        self.selector = BotSelector()
        self.selector.show()

    def send_welcome_message(self):
        messages = {
            "Optimus Prime": "Bien joué, humain. Tu as fait le bon choix en me sélectionnant.",
            "Megatron": "Excellent choix... tu sais reconnaître la vraie puissance.",
            "Bumblebee": "Salut ! Ensemble, on va faire un super duo !",
            "Starscream": "Héhé... tu ne le regretteras *peut-être* pas..."
        }
        welcome = messages.get(self.bot["name"], "Bienvenue !")
        self.add_bot_message(welcome)

    def handle_send(self):
        text = self.user_input.text().strip()
        if text:
            self.add_user_message(text)
            response = self.get_bot_response(text)
            self.add_bot_message(response)
            self.user_input.clear()

    def get_bot_response(self, message):
        try:
            if self.language == "fr":
                message = f"Tu es un robot qui répond uniquement en français. {message}"
            else:
                message = f"You are a chatbot that only responds in English. {message}"

            message_safe = shlex.quote(message)
            cmd = f'python app/chat_engine.py {message_safe}'
            result = subprocess.run(cmd, check=True, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            return f"[Erreur IA] {e}"

    def add_user_message(self, message):
        self.chat_display.append(f"<b>👤 Toi :</b> {message}")
        self.log.append(f"Toi: {message}")

    def add_bot_message(self, message):
        icon = self.get_bot_icon()
        formatted = f"<b>{icon} {self.bot['name']} :</b> {message}"
        self.chat_display.append(formatted)
        self.log.append(f"{self.bot['name']}: {message}")

    def restart_conversation(self):
        self.chat_display.clear()
        self.log.clear()
        self.send_welcome_message()

    def closeEvent(self, event):
        self.save_history()
        event.accept()

    def save_history(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_{self.bot['name'].lower()}_{now}.txt"
        path = os.path.join("chat_logs", filename)
        os.makedirs("chat_logs", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for line in self.log:
                f.write(line + "\n")

    def get_bot_icon(self):
        icons = {
            "Optimus Prime": "🤖",
            "Megatron": "🛡️",
            "Bumblebee": "🐝",
            "Starscream": "✈️"
        }
        return icons.get(self.bot["name"], "🤖")

    def get_persona(self, name):
        personas = {
            "Optimus Prime": "Je suis Optimus Prime. Je protège les humains avec sagesse et force.",
            "Megatron": "Je suis Megatron. Mon pouvoir est sans égal. Je ne tolère pas l'échec.",
            "Bumblebee": "Je suis Bumblebee ! Petit, rapide et toujours prêt à rigoler.",
            "Starscream": "Je suis Starscream. J'attends mon heure pour prendre le contrôle..."
        }
        return personas.get(name, "Je suis un bot Transformers.")