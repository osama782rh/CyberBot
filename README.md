# 🤖 CyberBot - Projet Python IA Transformers

**CyberBot** est un projet interactif alliant **chatbot intelligent** et **mini-jeu éducatif** dans l’univers des Transformers. Le joueur peut discuter avec un bot de son choix et participer à un combat de connaissances. L’application utilise une interface en **PyQt5** et un moteur de réponse **IA via Transformers**.

---

## ⚙️ Fonctionnalités principales

### 🏠 1. Écran d’accueil
Dès le lancement de l'application, l’utilisateur est accueilli par une animation stylisée et un fond Transformers spectaculaire.

<img src="assets/images/page_acceuil.png" alt="page_acceuil" width="200"/>


---

### 🤖 2. Sélection du bot
Le joueur peut faire défiler 4 bots emblématiques : **Optimus Prime**, **Megatron**, **Bumblebee**, **Starscream**. Chaque bot possède des caractéristiques uniques (forces, faiblesses, caractère…).

<img src="assets/images/selection_bot.png" alt="selection_bot" width="200"/>

---

### 🎯 3. Vue des compétences
Le bouton *Skills* permet d'afficher une fiche détaillée du bot sélectionné avec ses points forts et faibles, rendant le choix stratégique.

<img src="assets/images/skills.png" alt="skills" width="200"/>


---

### 💬 4. Mode Chat avec IA
Une fenêtre de discussion permet de parler librement avec le bot. L’utilisateur peut choisir la langue (**Français / Anglais**), et les réponses sont générées via **Transformers**.

<img src="assets/images/chat_bot.png" alt="chat_bot" width="200"/>


---

### 📂 5. Historique des discussions
Toutes les conversations sont enregistrées dans un dossier `chat_logs`, accessibles via un bouton. Idéal pour consulter ses anciennes discussions.

<img src="assets/images/chat_logs.png" alt="chat_logs" width="200"/>



---

### ⚔️ 6. Mode Combat VS
Un mini-jeu sous forme de **quiz interactif**. Le joueur affronte un autre bot et répond à des questions de culture générale (Python, math, culture tech…). Chaque bonne réponse augmente la puissance du joueur.

<img src="assets/images/mode_combat.png" alt="mode_combat" width="200"/>

---

## 🔧 Installation

```bash
git clone https://github.com/osama782rh/cyberbot.git
cd cyberbot
pip install -r requirements.txt
python main.py
```

---

## 🧠 Technologies utilisées

- Python 3
- PyQt5 (interface graphique)
- Transformers (moteur de réponse IA)
- Subprocess + Fichier `response.txt`
- Images & animations customisées