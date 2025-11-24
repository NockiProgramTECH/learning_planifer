"""Modèle pour la gestion des matières d'apprentissage"""

from datetime import datetime
from database.db_manager import DatabaseManager

class LearningSubject:
    """
    Représente une matière d'apprentissage.
    Gère le suivi du temps d'étude et la priorisation des matières.
    """
    
    @staticmethod
    def get_all_subjects():
        """
        Récupère toutes les matières d'apprentissage.
        
        Returns:
            list: Liste de toutes les matières
        """
        query = """
            SELECT * FROM learning_subjects 
            ORDER BY priority DESC, last_studied ASC NULLS FIRST
        """
        return DatabaseManager.execute_query(query, fetch=True)
    
    @staticmethod
    def get_subject_by_name(name):
        """
        Récupère une matière par son nom.
        
        Args:
            name (str): Nom de la matière
        
        Returns:
            dict: Informations de la matière
        """
        query = "SELECT * FROM learning_subjects WHERE name = %s"
        results = DatabaseManager.execute_query(query, (name,), fetch=True)
        return results[0] if results else None
    
    @staticmethod
    def update_study_time(subject_name, hours):
        """
        Met à jour le temps d'étude pour une matière.
        Incrémente le total et met à jour la dernière date d'étude.
        
        Args:
            subject_name (str): Nom de la matière
            hours (float): Nombre d'heures étudiées (peut être décimal)
        """
        query = """
            UPDATE learning_subjects 
            SET last_studied = NOW(), 
                total_hours = total_hours + %s
            WHERE name = %s
        """
        DatabaseManager.execute_query(query, (hours, subject_name))
    
    @staticmethod
    def get_least_studied(limit=8):
        """
        Récupère les matières les moins étudiées récemment.
        Utilisé pour prioriser les matières dans le planning.
        
        Args:
            limit (int): Nombre de matières à retourner
        
        Returns:
            list: Matières triées par ancienneté d'étude
        """
        query = """
            SELECT * FROM learning_subjects 
            ORDER BY 
                last_studied IS NULL DESC,  -- Jamais étudiées en premier
                last_studied ASC,           -- Puis les plus anciennes
                total_hours ASC             -- Puis celles avec moins d'heures
            LIMIT %s
        """
        return DatabaseManager.execute_query(query, (limit,), fetch=True)
    
    @staticmethod
    def get_most_studied(limit=5):
        """
        Récupère les matières les plus étudiées.
        
        Args:
            limit (int): Nombre de matières à retourner
        
        Returns:
            list: Matières triées par temps d'étude total
        """
        query = """
            SELECT * FROM learning_subjects 
            WHERE total_hours > 0
            ORDER BY total_hours DESC
            LIMIT %s
        """
        return DatabaseManager.execute_query(query, (limit,), fetch=True)
    
    @staticmethod
    def add_subject(name, priority=1):
        """
        Ajoute une nouvelle matière d'apprentissage.
        
        Args:
            name (str): Nom de la matière
            priority (int): Priorité (1-5, défaut: 1)
        
        Returns:
            int: ID de la matière créée
        """
        query = """
            INSERT INTO learning_subjects (name, priority)
            VALUES (%s, %s)
        """
        return DatabaseManager.execute_query(query, (name, priority))
    
    @staticmethod
    def delete_subject(subject_id):
        """
        Supprime une matière d'apprentissage.
        
        Args:
            subject_id (int): ID de la matière
        """
        query = "DELETE FROM learning_subjects WHERE id = %s"
        DatabaseManager.execute_query(query, (subject_id,))
    
    @staticmethod
    def update_priority(subject_name, priority):
        """
        Met à jour la priorité d'une matière.
        
        Args:
            subject_name (str): Nom de la matière
            priority (int): Nouvelle priorité (1-5)
        """
        query = "UPDATE learning_subjects SET priority = %s WHERE name = %s"
        DatabaseManager.execute_query(query, (priority, subject_name))
    
    @staticmethod
    def reset_study_time(subject_name):
        """
        Réinitialise le temps d'étude d'une matière.
        
        Args:
            subject_name (str): Nom de la matière
        """
        query = """
            UPDATE learning_subjects 
            SET total_hours = 0, last_studied = NULL
            WHERE name = %s
        """
        DatabaseManager.execute_query(query, (subject_name,))
    
    @staticmethod
    def get_statistics():
        """
        Récupère des statistiques sur l'apprentissage.
        
        Returns:
            dict: Statistiques globales
        """
        stats = {}
        
        # Total de matières
        query = "SELECT COUNT(*) as count FROM learning_subjects"
        result = DatabaseManager.execute_query(query, fetch=True)
        stats['total_subjects'] = result[0]['count'] if result else 0
        
        # Total d'heures étudiées
        query = "SELECT SUM(total_hours) as total FROM learning_subjects"
        result = DatabaseManager.execute_query(query, fetch=True)
        stats['total_hours'] = float(result[0]['total'] or 0)
        
        # Matières jamais étudiées
        query = "SELECT COUNT(*) as count FROM learning_subjects WHERE last_studied IS NULL"
        result = DatabaseManager.execute_query(query, fetch=True)
        stats['never_studied'] = result[0]['count'] if result else 0
        
        # Moyenne d'heures par matière
        if stats['total_subjects'] > 0:
            stats['avg_hours_per_subject'] = stats['total_hours'] / stats['total_subjects']
        else:
            stats['avg_hours_per_subject'] = 0
        
        return stats
    
    @staticmethod
    def get_balanced_distribution(available_slots):
        """
        Distribue équitablement les créneaux disponibles entre toutes les matières.
        Algorithme de rotation pour assurer l'équilibre.
        
        Args:
            available_slots (int): Nombre de créneaux disponibles
        
        Returns:
            list: Liste de noms de matières dans l'ordre de priorité
        """
        subjects = LearningSubject.get_least_studied()
        
        if not subjects:
            return []
        
        # Créer une distribution équitable
        distribution = []
        subject_index = 0
        
        for _ in range(available_slots):
            distribution.append(subjects[subject_index % len(subjects)]['name'])
            subject_index += 1
        
        return distribution