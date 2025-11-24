# 📚 Learning Planner - Planificateur d'Apprentissage Intelligent

## 🎯 Description

Un système complet de gestion automatique de planning d'apprentissage avec interface graphique moderne. Le programme gère vos cours, devoirs et répartit intelligemment l'apprentissage de 8 matières avec notifications desktop.

### ✨ Fonctionnalités principales

- ✅ **Gestion des cours** - Ajout facile de vos cours hebdomadaires
- ✅ **Gestion des devoirs** - Suivi des échéances avec planification automatique
- ✅ **8 matières d'apprentissage** - Répartition équitable et intelligente
- ✅ **Notifications desktop** - Rappels 15 minutes avant chaque activité
- ✅ **Révisions automatiques** - Détection des cours à réviser (>7 jours)
- ✅ **Interface moderne** - CustomTkinter avec design professionnel
- ✅ **Base MySQL** - Stockage robuste et performant

## 📋 Matières gérées

- 🐍 Python
- 🌐 HTML
- 🎨 CSS
- 🔧 PHP
- 🗄️ MySQL
- 🐘 PostgreSQL
- 📐 Mathématiques Générales
- 📖 Lecture de la Bible

## 📁 Structure du projet

```
learning_planner/
│
├── main.py                    # Point d'entrée de l'application
├── config.py                  # Configuration (DB, paramètres)
├── requirements.txt           # Dépendances Python
├── README.md                  # Ce fichier
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py         # Gestionnaire de connexion MySQL
│   └── schema.sql            # Structure de la base de données
│
├── models/
│   ├── __init__.py
│   ├── course.py             # Modèle des cours
│   ├── homework.py           # Modèle des devoirs
│   └── learning.py           # Modèle des matières
│
├── services/
│   ├── __init__.py
│   ├── scheduler.py          # Algorithme de planification intelligent
│   └── notification.py       # Service de notifications desktop
│
└── gui/
    ├── __init__.py
    ├── main_window.py        # Fenêtre principale
    ├── course_manager.py     # Interface gestion des cours
    ├── homework_manager.py   # Interface gestion des devoirs
    └── schedule_viewer.py    # Visualisation du planning
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- MySQL Server 5.7 ou supérieur
- Système d'exploitation : Windows 10/11, Linux, macOS

### Étape 1 : Installer Python

Téléchargez et installez Python depuis [python.org](https://www.python.org/downloads/)

Vérifiez l'installation :
```bash
python --version
```

### Étape 2 : Installer MySQL

#### Windows
1. Téléchargez [MySQL Installer](https://dev.mysql.com/downloads/installer/)
2. Installez MySQL Server
3. Notez le mot de passe root défini pendant l'installation

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### macOS
```bash
brew install mysql
brew services start mysql
```

Vérifiez l'installation :
```bash
mysql --version
```

### Étape 3 : Créer la base de données

1. Connectez-vous à MySQL :
```bash
mysql -u root -p
```

2. Créez la base de données :
```sql
CREATE DATABASE learning_planner CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

3. Importez le schéma :
```bash
mysql -u root -p learning_planner < database/schema.sql
```

### Étape 4 : Installer les dépendances Python

```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 5 : Configuration

Modifiez le fichier `config.py` avec vos identifiants MySQL :

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # VOTRE utilisateur MySQL
    'password': 'votre_mdp', # VOTRE mot de passe MySQL
    'database': 'learning_planner',
    'charset': 'utf8mb4'
}
```

### Étape 6 : Lancer l'application

```bash
python main.py
```

## 📖 Guide d'utilisation

### 📅 Chaque samedi (planification hebdomadaire)

1. **Ouvrir "Gestion des Cours"**
   - Cliquez sur le bouton dans le menu latéral
   - Ajoutez tous vos cours de la semaine suivante
   - Exemple : "Architecture des Ordinateurs, Lundi, 14:00, 18:00"

2. **Ouvrir "Gestion des Devoirs"**
   - Ajoutez vos devoirs avec dates limites
   - Exemple : "Technologie IP, Jeudi, 14:00"
   - Définissez le nombre de jours de préparation (défaut : 3)

3. **Générer le planning**
   - Cliquez sur "🔄 Générer Planning"
   - Le système crée automatiquement votre emploi du temps
   - Les devoirs urgents sont priorisés
   - Les révisions sont planifiées
   - Les 8 matières sont réparties équitablement

4. **Consulter votre planning**
   - Allez dans "📊 Planning Semaine"
   - Naviguez entre les semaines
   - Visualisez toutes vos activités

### 🔔 Au quotidien

- Les notifications apparaissent automatiquement 15 minutes avant chaque activité
- Consultez votre planning pour voir ce qui vous attend
- Le système gère tout en arrière-plan

## 🧮 Algorithme de planification

### Priorités

1. **🔴 Priorité maximale : Devoirs urgents** (≤3 jours)
   - Alloués en premier
   - Sessions de 1h30
   - Répartis sur plusieurs jours si nécessaire

2. **🟠 Priorité haute : Révisions** (cours >7 jours)
   - Planifiées en début de semaine
   - Sessions de 1h30
   - Maximum 1 révision par jour

3. **🟢 Priorité normale : Apprentissage**
   - Répartition équitable des 8 matières
   - Rotation pour éviter la monotonie
   - Sessions de 1h30
   - Pauses de 15 minutes entre sessions

### Contraintes respectées

- Journée : 6h00 - 23h00
- Pause déjeuner : 12h00 - 13h00
- Pause dîner : 19h00 - 20h00
- Sessions : 1h30 (configurable)
- Pauses : 15 minutes entre sessions

## 🔧 Configuration avancée

### Modifier les paramètres dans `config.py`

```python
PLANNING_CONFIG = {
    'day_start': '06:00',           # Heure de début de journée
    'day_end': '23:00',             # Heure de fin de journée
    'lunch_break': ('12:00', '13:00'),
    'dinner_break': ('19:00', '20:00'),
    'session_duration': 90,          # Durée en minutes
    'break_duration': 15,            # Pause en minutes
    'homework_preparation_days': 3,  # Jours avant devoir
    'revision_threshold_days': 7     # Jours avant révision
}
```

### Ajouter/Modifier les matières

Modifiez `LEARNING_SUBJECTS` dans `config.py` :

```python
LEARNING_SUBJECTS = [
    'Python',
    'HTML',
    'CSS',
    # Ajoutez vos matières ici
]
```

## 🐛 Dépannage

### Erreur : "Impossible de se connecter à la base de données"

1. Vérifiez que MySQL est démarré :
```bash
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql

# macOS
brew services start mysql
```

2. Vérifiez les identifiants dans `config.py`
3. Vérifiez que la base de données existe :
```bash
mysql -u root -p -e "SHOW DATABASES;"
```

### Erreur : "Module not found"

Réinstallez les dépendances :
```bash
pip install -r requirements.txt --upgrade
```

### Les notifications ne fonctionnent pas

- **Windows** : Vérifiez que les notifications sont activées dans les paramètres système
- **Linux** : Installez `libnotify` : `sudo apt install libnotify-bin`
- **macOS** : Autorisez les notifications dans Préférences Système

### L'interface ne s'affiche pas correctement

Mettez à jour CustomTkinter :
```bash
pip install customtkinter --upgrade
```

## 📊 Exemple d'utilisation

### Scénario concret

**Lundi :**
- 14h00-18h00 : Cours d'Architecture des Ordinateurs (ajouté manuellement)
- 08h00-09h30 : Apprentissage Python (généré automatiquement)
- 10h00-11h30 : Apprentissage HTML (généré automatiquement)

**Jeudi :**
- 14h00-18h00 : Devoir Technologie IP (ajouté manuellement)
- 08h00-09h30 : Préparation devoir (3 jours avant - automatique)
- 10h00-11h30 : Apprentissage CSS (généré automatiquement)

**Autres jours :**
- Le système remplit automatiquement avec :
  - Révisions des cours passés
  - Apprentissage rotatif des 8 matières
  - Respect des pauses et des horaires

## 🤝 Contribution

Ce projet est personnel mais les suggestions sont bienvenues !

## 📝 Licence

© 2024 - Usage personnel

## 📧 Support

Pour toute question ou problème :
- Consultez ce README
- Vérifiez la configuration dans `config.py`
- Vérifiez les logs dans la console

## 🎉 Bon apprentissage !

Que votre parcours d'apprentissage soit productif et organisé ! 📚✨