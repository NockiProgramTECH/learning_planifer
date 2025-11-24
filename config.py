"""Configuration de la base de données et paramètres globaux"""

# Configuration de la base de données MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # MODIFIER avec votre utilisateur MySQL
    'password': 'Unixdev38</>',  # MODIFIER avec votre mot de passe MySQL
    'database': 'learning_planner',
    'charset': 'utf8mb4'
}

# Matières d'apprentissage
LEARNING_SUBJECTS = [
    'Python',
    'HTML',
    'CSS',
    'PHP',
    'MySQL',
    'PostgreSQL',
    'Math_General',
    'Lire_la_Bible'
]

# Paramètres de planification
PLANNING_CONFIG = {
    'day_start': '06:00',           # Début de journée
    'day_end': '23:00',             # Fin de journée
    'lunch_break': ('12:00', '13:00'),   # Pause déjeuner
    'dinner_break': ('19:00', '20:00'),  # Pause dîner
    'session_duration': 90,          # Durée d'une session en minutes
    'break_duration': 15,            # Durée d'une pause en minutes
    'homework_preparation_days': 3,  # Jours avant un devoir pour commencer
    'revision_threshold_days': 7     # Jours avant de réviser un cours
}

# Paramètres de notification
NOTIFICATION_CONFIG = {
    'enabled': True,
    'advance_minutes': 15,  # Notifier X minutes avant
    'sound': True,
    'timeout': 10  # Durée d'affichage en secondes
}