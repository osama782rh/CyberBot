from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import random

class CombatWindow(QWidget):
    def __init__(self, player_bot, enemy_bot):
        super().__init__()
        self.setWindowTitle("CyberCombat - VS Mode")
        self.setFixedSize(800, 1000)
        self.setStyleSheet("background-color: white; color: #003366;")

        self.player_bot = player_bot
        self.enemy_bot = enemy_bot

        self.player_power = 50
        self.enemy_power = 50

        self.questions = [
            {"q": "Quelle est la sortie de 2 ** 3 ?", "a": "8"},
            {"q": "Quel est le langage utilisé pour TensorFlow ?", "a": "python"},
            {"q": "Combien de bits dans un octet ?", "a": "8"},
            {"q": "Qui est l'ennemi juré d'Optimus Prime ?", "a": "megatron"},
            {"q": "Quel mot-clé pour une fonction en Python ?", "a": "def"},
            {"q": "Combien de côtés a un hexagone ?", "a": "6"},
            {"q": "Quelle planète est la plus proche du Soleil ?", "a": "mercure"},
            {"q": "Combien vaut 3 x 4 ?", "a": "12"},
            {"q": "Quel est le nom complet de HTML ?", "a": "hypertext markup language"},
            {"q": "Quel est l'inverse de 'True' en Python ?", "a": "false"}
        ]

        self.init_ui()
        self.load_new_question()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel(f"\U0001f31f CyberCombat\n{self.player_bot['name']} VS {self.enemy_bot['name']} \U0001f31f")
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setFont(QFont("Orbitron", 28, QFont.Bold))
        title.setStyleSheet("color: #004080;")
        layout.addWidget(title)

        power_layout = QHBoxLayout()

        self.player_status = QLabel()
        self.player_status.setAlignment(Qt.AlignCenter)
        self.player_status.setFont(QFont("Arial", 18))

        self.enemy_status = QLabel()
        self.enemy_status.setAlignment(Qt.AlignCenter)
        self.enemy_status.setFont(QFont("Arial", 18))

        power_layout.addWidget(self.player_status)
        power_layout.addStretch()
        power_layout.addWidget(self.enemy_status)

        layout.addLayout(power_layout)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.question_label = QLabel("Question")
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont("Arial", 18))
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("margin: 20px;")

        layout.addWidget(self.question_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        answer_layout = QHBoxLayout()
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Tape ta réponse ici...")
        self.answer_input.returnPressed.connect(self.check_answer)
        self.answer_input.setFont(QFont("Arial", 14))
        self.answer_input.setStyleSheet("padding: 6px; border-radius: 8px; border: 2px solid #0066cc; background-color: #eef6fb; color: #003366;")

        self.submit_btn = QPushButton("Valider")
        self.submit_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.submit_btn.setStyleSheet("background-color: #d9eaff; color: #003366; border: 2px solid #0066cc; border-radius: 8px;")
        self.submit_btn.clicked.connect(self.check_answer)

        answer_layout.addWidget(self.answer_input)
        answer_layout.addWidget(self.submit_btn)

        layout.addLayout(answer_layout)

        controls = QHBoxLayout()
        self.next_btn = QPushButton("🔁 Nouvelle Question")
        self.next_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.next_btn.setStyleSheet("background-color: #f0f8ff; color: #003366; border-radius: 8px; padding: 8px;")
        self.next_btn.clicked.connect(self.load_new_question)

        self.finish_btn = QPushButton("🏆 Terminer le Combat")
        self.finish_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.finish_btn.setStyleSheet("background-color: #cc0000; color: white; border-radius: 8px; padding: 8px;")
        self.finish_btn.clicked.connect(self.finish_fight)

        self.back_btn = QPushButton("⬅ Retour")
        self.back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.back_btn.setStyleSheet("background-color: #cccccc; color: black; border-radius: 8px; padding: 8px;")
        self.back_btn.clicked.connect(self.go_back)

        controls.addWidget(self.back_btn)
        controls.addWidget(self.next_btn)
        controls.addStretch()
        controls.addWidget(self.finish_btn)

        layout.addLayout(controls)
        self.setLayout(layout)
        self.update_power_display()

    def load_new_question(self):
        self.current_q = random.choice(self.questions)
        self.question_label.setText(f"\U0001f9d0 {self.current_q['q']}")
        self.answer_input.clear()

    def check_answer(self):
        user_answer = self.answer_input.text().strip().lower()
        correct = self.current_q['a'].strip().lower()
        if user_answer == correct:
            self.player_power += 10
            QMessageBox.information(self, "✅ Bonne réponse !", "Ton bot devient plus fort !")
        else:
            self.enemy_power += 5
            QMessageBox.warning(self, "❌ Mauvaise réponse", "L'ennemi en profite pour gagner en puissance...")
        self.update_power_display()
        self.load_new_question()

    def update_power_display(self):
        self.player_status.setText(f"{self.player_bot['name']}\n💪 Puissance : {self.player_power}")
        self.enemy_status.setText(f"{self.enemy_bot['name']}\n💪 Puissance : {self.enemy_power}")

    def finish_fight(self):
        if self.player_power > self.enemy_power:
            result = f"\U0001f389 Victoire de {self.player_bot['name']} !"
        elif self.player_power < self.enemy_power:
            result = f"❌ {self.enemy_bot['name']} l'emporte..."
        else:
            result = "\U0001f504 Égalité parfaite !"

        QMessageBox.information(self, "Résultat du combat", result)
        self.close()

    def go_back(self):
        from app.bot_selector import BotSelector
        self.close()
        self.selector = BotSelector()
        self.selector.show()