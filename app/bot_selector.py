from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from app.combat_window import CombatWindow
from app.chat_window import ChatWindow


class BotSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberBot - Sélectionnez votre bot")
        self.setFixedSize(800, 1000)
        self.setStyleSheet("background-color: white; color: #001f3f;")

        self.bots = [
            {
                "name": "Optimus Prime",
                "image": "assets/images/optimus.jpg",
                "skills": {
                    "character": "Leader noble et protecteur",
                    "strengths": ["Stratégie", "Force brute", "Leadership"],
                    "weaknesses": ["Trop empathique", "Prévisible"]
                }
            },
            {
                "name": "Megatron",
                "image": "assets/images/megatron.jpg",
                "skills": {
                    "character": "Froid, calculateur et dominant",
                    "strengths": ["Ruse", "Puissance", "Détermination"],
                    "weaknesses": ["Arrogance", "Colère"]
                }
            },
            {
                "name": "Bumblebee",
                "image": "assets/images/bumblebee.jpg",
                "skills": {
                    "character": "Loyal, agile et joueur",
                    "strengths": ["Vitesse", "Discrétion", "Communication"],
                    "weaknesses": ["Taille", "Fragilité"]
                }
            },
            {
                "name": "Starscream",
                "image": "assets/images/starscream.jpg",
                "skills": {
                    "character": "Ambitieux et traître",
                    "strengths": ["Vol", "Attaques aériennes", "Manipulation"],
                    "weaknesses": ["Lâcheté", "Manque de loyauté"]
                }
            }
        ]

        self.current_index = 0
        self.showing_skills = False

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel("")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setFont(QFont("Orbitron", 36, QFont.Bold))
        self.name_label.setStyleSheet("color: #003366;")

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.skills_text = QLabel()
        self.skills_text.setWordWrap(True)
        self.skills_text.setAlignment(Qt.AlignTop)
        self.skills_text.setFont(QFont("Arial", 16))
        self.skills_text.setStyleSheet("margin: 20px; background-color: #f0f8ff; color: #001f3f; border-radius: 10px; padding: 15px; border: 1px solid #ccc;")
        self.skills_text.hide()

        arrow_layout = QHBoxLayout()
        self.left_btn = QPushButton("←")
        self.right_btn = QPushButton("→")
        self.skills_btn = QPushButton("Skills")

        for btn in [self.left_btn, self.right_btn, self.skills_btn]:
            btn.setFixedSize(100, 40)
            btn.setFont(QFont("Arial", 12, QFont.Bold))
            btn.setStyleSheet("background-color: #0074D9; color: white; border: none; border-radius: 10px;")

        self.left_btn.clicked.connect(self.prev_bot)
        self.right_btn.clicked.connect(self.next_bot)
        self.skills_btn.clicked.connect(self.toggle_skills)

        arrow_layout.addWidget(self.left_btn)
        arrow_layout.addStretch()
        arrow_layout.addWidget(self.skills_btn)
        arrow_layout.addStretch()
        arrow_layout.addWidget(self.right_btn)

        self.choose_btn = QPushButton("Choisir ce bot")
        self.choose_btn.setFixedHeight(40)
        self.choose_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.choose_btn.setStyleSheet("background-color: #ffffff; color: #001f3f; border: 2px solid #001f3f; border-radius: 10px;")
        self.choose_btn.clicked.connect(self.select_bot)

        self.fight_btn = QPushButton("Mode Combat VS")
        self.fight_btn.setFixedHeight(40)
        self.fight_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.fight_btn.setStyleSheet("background-color: #FF4136; color: white; border: none; border-radius: 10px;")
        self.fight_btn.clicked.connect(self.launch_combat)

        self.layout.addStretch()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.skills_text)
        self.layout.addLayout(arrow_layout)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.choose_btn)
        self.layout.addWidget(self.fight_btn)
        self.layout.addStretch()

    def update_display(self):
        bot = self.bots[self.current_index]
        self.name_label.setText(bot["name"])
        self.showing_skills = False
        self.image_label.show()
        self.skills_text.hide()

        pixmap = QPixmap(bot["image"])
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

    def toggle_skills(self):
        bot = self.bots[self.current_index]
        if self.showing_skills:
            self.update_display()
        else:
            self.image_label.hide()
            self.skills_text.show()

            info = f"\U0001f9e0 <b>Caractère :</b> {bot['skills']['character']}<br><br>"
            info += "<span style='color:green;'>✅ <b>Points forts :</b></span><br>"
            for s in bot['skills']['strengths']:
                info += f"• {s}<br>"
            info += "<br><span style='color:red;'>⚠️ <b>Faiblesses :</b></span><br>"
            for w in bot['skills']['weaknesses']:
                info += f"• {w}<br>"

            self.skills_text.setText(info)
            self.showing_skills = True

    def next_bot(self):
        self.current_index = (self.current_index + 1) % len(self.bots)
        self.update_display()

    def prev_bot(self):
        self.current_index = (self.current_index - 1) % len(self.bots)
        self.update_display()

    def select_bot(self):
        selected_bot = self.bots[self.current_index]
        print(f"✅ Bot sélectionné : {selected_bot['name']}")
        self.hide()
        self.chat_window = ChatWindow(selected_bot)
        self.chat_window.show()

    def launch_combat(self):
        player_bot = self.bots[self.current_index]
        enemy_index = (self.current_index + 1) % len(self.bots)
        enemy_bot = self.bots[enemy_index]
        print(f"⚔️ Combat lancé : {player_bot['name']} VS {enemy_bot['name']}")
        self.hide()
        self.combat_window = CombatWindow(player_bot, enemy_bot)
        self.combat_window.show()
