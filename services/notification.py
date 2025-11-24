"""Service de notifications desktop Windows"""

from plyer import notification
from datetime import datetime, timedelta
import threading
import time
from database.db_manager import DatabaseManager
from config import NOTIFICATION_CONFIG

class NotificationService:
    """
    Gère les notifications desktop pour rappeler les activités.
    Fonctionne en arrière-plan pour surveiller le planning.
    """
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.enabled = NOTIFICATION_CONFIG['enabled']
    
    def start(self):
        """Démarre le service de notifications en arrière-plan"""
        if not self.running and self.enabled:
            self.running = True
            self.thread = threading.Thread(target=self._notification_loop, daemon=True)
            self.thread.start()
            print("🔔 Service de notifications démarré")
    
    def stop(self):
        """Arrête le service de notifications"""
        if self.running:
            self.running = False
            print("🔕 Service de notifications arrêté")
    
    def enable(self):
        """Active les notifications"""
        self.enabled = True
        if not self.running:
            self.start()
    
    def disable(self):
        """Désactive les notifications"""
        self.enabled = False
        self.stop()
    
    def _notification_loop(self):
        """
        Boucle principale qui vérifie les activités à venir.
        S'exécute toutes les minutes.
        """
        print("🔄 Boucle de notifications active")
        
        while self.running:
            try:
                self._check_upcoming_activities()
                time.sleep(60)  # Vérifier chaque minute
            except Exception as e:
                print(f"❌ Erreur dans la boucle de notification: {e}")
                time.sleep(60)
    
    def _check_upcoming_activities(self):
        """
        Vérifie les activités qui commencent dans les X prochaines minutes
        et envoie des notifications pour celles qui n'ont pas encore été notifiées.
        """
        now = datetime.now()
        advance_minutes = NOTIFICATION_CONFIG['advance_minutes']
        notification_window_start = now
        notification_window_end = now + timedelta(minutes=advance_minutes + 1)
        
        # Requête pour trouver les activités à notifier
        query = """
            SELECT * FROM schedule_slots 
            WHERE date = %s 
            AND start_time >= %s 
            AND start_time <= %s
            AND notified = FALSE
            ORDER BY start_time
        """
        
        activities = DatabaseManager.execute_query(
            query, 
            (
                now.date(), 
                notification_window_start.time(), 
                notification_window_end.time()
            ),
            fetch=True
        )
        
        for activity in activities:
            # Calculer le temps restant
            activity_start = datetime.combine(
                activity['date'], 
                activity['start_time']
            )
            minutes_until = (activity_start - now).total_seconds() / 60
            
            # Ne notifier que si c'est dans la fenêtre de notification
            if 0 <= minutes_until <= advance_minutes:
                self._send_notification(activity, int(minutes_until))
                self._mark_as_notified(activity['id'])
    
    def _send_notification(self, activity, minutes_until):
        """
        Envoie une notification desktop pour une activité.
        
        Args:
            activity (dict): Informations de l'activité
            minutes_until (int): Minutes avant le début
        """
        # Icônes selon le type d'activité
        icons = {
            'course': '🎓',
            'homework': '✏️',
            'learning': '📚',
            'revision': '🔄'
        }
        
        icon = icons.get(activity['activity_type'], '📌')
        
        # Construire le message
        if minutes_until == 0:
            title = f"{icon} C'EST MAINTENANT !"
            time_msg = "commence maintenant"
        elif minutes_until == 1:
            title = f"{icon} Dans 1 minute"
            time_msg = "commence dans 1 minute"
        else:
            title = f"{icon} Dans {minutes_until} minutes"
            time_msg = f"commence dans {minutes_until} minutes"
        
        # Type d'activité en français
        activity_types = {
            'course': 'Cours',
            'homework': 'Devoir',
            'learning': 'Apprentissage',
            'revision': 'Révision'
        }
        activity_label = activity_types.get(activity['activity_type'], 'Activité')
        
        message = f"{activity_label}: {activity['subject']}\n{time_msg}"
        
        # Afficher aussi dans la console
        print(f"🔔 Notification: {title} - {message}")
        
        # Envoyer la notification
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="📚 Learning Planner",
                timeout=NOTIFICATION_CONFIG['timeout']
            )
        except Exception as e:
            print(f"❌ Erreur envoi notification: {e}")
    
    def _mark_as_notified(self, schedule_id):
        """
        Marque une activité comme ayant été notifiée.
        
        Args:
            schedule_id (int): ID du créneau dans schedule_slots
        """
        query = "UPDATE schedule_slots SET notified = TRUE WHERE id = %s"
        DatabaseManager.execute_query(query, (schedule_id,))
    
    def send_test_notification(self):
        """Envoie une notification de test"""
        try:
            notification.notify(
                title="🧪 Test de notification",
                message="Les notifications fonctionnent correctement !",
                app_name="📚 Learning Planner",
                timeout=10
            )
            print("✅ Notification de test envoyée")
            return True
        except Exception as e:
            print(f"❌ Échec du test de notification: {e}")
            return False
    
    def get_today_schedule(self):
        """
        Récupère le planning du jour pour aperçu rapide.
        
        Returns:
            list: Activités du jour
        """
        today = datetime.now().date()
        query = """
            SELECT * FROM schedule_slots 
            WHERE date = %s 
            ORDER BY start_time
        """
        return DatabaseManager.execute_query(query, (today,), fetch=True)
    
    def send_daily_summary(self):
        """
        Envoie un résumé du planning de la journée.
        Utile à lancer le matin.
        """
        activities = self.get_today_schedule()
        
        if not activities:
            notification.notify(
                title="📅 Planning du jour",
                message="Aucune activité planifiée aujourd'hui",
                app_name="📚 Learning Planner",
                timeout=10
            )
            return
        
        # Compter par type
        counts = {}
        for activity in activities:
            act_type = activity['activity_type']
            counts[act_type] = counts.get(act_type, 0) + 1
        
        # Construire le message
        parts = []
        labels = {
            'course': '🎓 Cours',
            'homework': '✏️ Devoirs',
            'learning': '📚 Apprentissage',
            'revision': '🔄 Révisions'
        }
        
        for act_type, count in counts.items():
            parts.append(f"{labels.get(act_type, act_type)}: {count}")
        
        message = "\n".join(parts)
        message += f"\n\nTotal: {len(activities)} activités"
        
        notification.notify(
            title="📅 Votre planning d'aujourd'hui",
            message=message,
            app_name="📚 Learning Planner",
            timeout=15
        )
        
        print(f"📊 Résumé du jour envoyé: {len(activities)} activités")