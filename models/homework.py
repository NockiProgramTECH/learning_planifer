"""Modèle pour la gestion des devoirs"""

from datetime import datetime, timedelta, date
from database.db_manager import DatabaseManager

class Homework:
    """
    Représente un devoir à rendre.
    Gère l'ajout, le suivi et les alertes pour les devoirs.
    """
    
    @staticmethod
    def add_homework(subject, description, due_date, due_time, preparation_days=3):
        """
        Ajoute un nouveau devoir dans la base de données.
        
        Args:
            subject (str): Matière du devoir (ex: "Technologie IP")
            description (str): Description du devoir
            due_date (str): Date limite au format YYYY-MM-DD
            due_time (str): Heure limite au format HH:MM
            preparation_days (int): Nombre de jours pour préparer (défaut: 3)
        
        Returns:
            int: ID du devoir créé
        """
        query = """
            INSERT INTO homework 
            (subject, description, due_date, due_time, preparation_days, status)
            VALUES (%s, %s, %s, %s, %s, 'pending')
        """
        return DatabaseManager.execute_query(
            query, (subject, description, due_date, due_time, preparation_days)
        )
    
    @staticmethod
    def get_pending_homework():
        """
        Récupère tous les devoirs en attente ou en cours.
        
        Returns:
            list: Liste des devoirs non terminés
        """
        query = """
            SELECT * FROM homework 
            WHERE status != 'completed' AND due_date >= CURDATE()
            ORDER BY due_date ASC, due_time ASC
        """
        return DatabaseManager.execute_query(query, fetch=True)
    
    @staticmethod
    def get_all_homework():
        """
        Récupère tous les devoirs (incluant terminés).
        
        Returns:
            list: Liste complète des devoirs
        """
        query = """
            SELECT * FROM homework 
            ORDER BY due_date DESC, due_time DESC
        """
        return DatabaseManager.execute_query(query, fetch=True)
    
    @staticmethod
    def get_urgent_homework(days_threshold=3):
        """
        Récupère les devoirs urgents (dans X jours ou moins).
        Ces devoirs doivent être priorisés dans le planning.
        
        Args:
            days_threshold (int): Nombre de jours pour considérer comme urgent
        
        Returns:
            list: Liste des devoirs urgents
        """
        query = """
            SELECT * FROM homework 
            WHERE status != 'completed' 
            AND DATEDIFF(due_date, CURDATE()) <= %s
            AND due_date >= CURDATE()
            ORDER BY due_date ASC, due_time ASC
        """
        return DatabaseManager.execute_query(query, (days_threshold,), fetch=True)
    
    @staticmethod
    def get_homework_needing_preparation():
        """
        Récupère les devoirs qui nécessitent de commencer la préparation maintenant.
        Basé sur le nombre de jours de préparation configurés.
        
        Returns:
            list: Liste des devoirs à préparer
        """
        query = """
            SELECT * FROM homework 
            WHERE status = 'pending'
            AND DATEDIFF(due_date, CURDATE()) <= preparation_days
            AND due_date >= CURDATE()
            ORDER BY due_date ASC
        """
        return DatabaseManager.execute_query(query, fetch=True)
    
    @staticmethod
    def update_status(homework_id, status):
        """
        Met à jour le statut d'un devoir.
        
        Args:
            homework_id (int): ID du devoir
            status (str): Nouveau statut ('pending', 'in_progress', 'completed')
        """
        query = "UPDATE homework SET status = %s WHERE id = %s"
        DatabaseManager.execute_query(query, (status, homework_id))
    
    @staticmethod
    def delete_homework(homework_id):
        """
        Supprime un devoir de la base de données.
        
        Args:
            homework_id (int): ID du devoir à supprimer
        """
        query = "DELETE FROM homework WHERE id = %s"
        DatabaseManager.execute_query(query, (homework_id,))
    
    @staticmethod
    def get_homework_by_id(homework_id):
        """
        Récupère un devoir spécifique par son ID.
        
        Args:
            homework_id (int): ID du devoir
        
        Returns:
            dict: Informations du devoir
        """
        query = "SELECT * FROM homework WHERE id = %s"
        results = DatabaseManager.execute_query(query, (homework_id,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def get_overdue_homework():
        """
        Récupère les devoirs en retard (date limite passée).
        
        Returns:
            list: Liste des devoirs en retard
        """
        query = """
            SELECT * FROM homework 
            WHERE status != 'completed' 
            AND due_date < CURDATE()
            ORDER BY due_date DESC
        """
        return DatabaseManager.execute_query(query, fetch=True)
    
    @staticmethod
    def update_homework(homework_id, subject=None, description=None, 
                       due_date=None, due_time=None, preparation_days=None):
        """
        Met à jour les informations d'un devoir.
        
        Args:
            homework_id (int): ID du devoir
            subject (str, optional): Nouvelle matière
            description (str, optional): Nouvelle description
            due_date (str, optional): Nouvelle date limite
            due_time (str, optional): Nouvelle heure limite
            preparation_days (int, optional): Nouveau nombre de jours de préparation
        """
        updates = []
        params = []
        
        if subject:
            updates.append("subject = %s")
            params.append(subject)
        if description is not None:  # Peut être une chaîne vide
            updates.append("description = %s")
            params.append(description)
        if due_date:
            updates.append("due_date = %s")
            params.append(due_date)
        if due_time:
            updates.append("due_time = %s")
            params.append(due_time)
        if preparation_days:
            updates.append("preparation_days = %s")
            params.append(preparation_days)
        
        if updates:
            params.append(homework_id)
            query = f"UPDATE homework SET {', '.join(updates)} WHERE id = %s"
            DatabaseManager.execute_query(query, tuple(params))
    
    @staticmethod
    def get_statistics():
        """
        Récupère des statistiques sur les devoirs.
        
        Returns:
            dict: Statistiques (total, complétés, en cours, en retard)
        """
        stats = {
            'total': 0,
            'completed': 0,
            'in_progress': 0,
            'pending': 0,
            'overdue': 0
        }
        
        # Total
        query = "SELECT COUNT(*) as count FROM homework"
        result = DatabaseManager.execute_query(query, fetch=True)
        stats['total'] = result[0]['count'] if result else 0
        
        # Par statut
        query = "SELECT status, COUNT(*) as count FROM homework GROUP BY status"
        results = DatabaseManager.execute_query(query, fetch=True)
        for row in results:
            stats[row['status']] = row['count']
        
        # En retard
        query = """
            SELECT COUNT(*) as count FROM homework 
            WHERE status != 'completed' AND due_date < CURDATE()
        """
        result = DatabaseManager.execute_query(query, fetch=True)
        stats['overdue'] = result[0]['count'] if result else 0
        
        return stats