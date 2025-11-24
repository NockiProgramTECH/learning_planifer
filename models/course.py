"""Modèle pour la gestion des cours"""

from datetime import datetime, date, timedelta
from database.db_manager import DatabaseManager

class Course:
    """
    Représente un cours universitaire.
    Gère l'ajout, la récupération et le suivi des cours.
    """
    
    @staticmethod
    def add_course(name, day_of_week, start_time, end_time, week_date):
        """
        Ajoute un nouveau cours dans la base de données.
        
        Args:
            name (str): Nom du cours (ex: "Architecture des Ordinateurs")
            day_of_week (str): Jour de la semaine (ex: "Lundi")
            start_time (str): Heure de début au format HH:MM (ex: "14:00")
            end_time (str): Heure de fin au format HH:MM (ex: "18:00")
            week_date (str): Date du début de la semaine YYYY-MM-DD
        
        Returns:
            int: ID du cours créé
        """
        query = """
            INSERT INTO courses (name, day_of_week, start_time, end_time, week_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        return DatabaseManager.execute_query(
            query, (name, day_of_week, start_time, end_time, week_date)
        )
    
    @staticmethod
    def get_courses_by_week(week_start_date):
        """
        Récupère tous les cours d'une semaine donnée.
        
        Args:
            week_start_date (date): Date du lundi de la semaine
        
        Returns:
            list: Liste des cours de la semaine
        """
        query = """
            SELECT * FROM courses 
            WHERE week_date >= %s AND week_date < DATE_ADD(%s, INTERVAL 7 DAY)
            ORDER BY week_date, start_time
        """
        return DatabaseManager.execute_query(
            query, (week_start_date, week_start_date), fetch=True
        )
    
    @staticmethod
    def get_all_courses():
        """
        Récupère tous les cours enregistrés.
        
        Returns:
            list: Liste complète des cours
        """
        query = "SELECT * FROM courses ORDER BY week_date DESC, start_time"
        return DatabaseManager.execute_query(query, fetch=True)
    
    @staticmethod
    def get_courses_for_revision():
        """
        Récupère les cours qui nécessitent une révision.
        Un cours nécessite une révision s'il date de plus de 7 jours
        et n'a pas encore été marqué comme révisé.
        
        Returns:
            list: Liste des cours à réviser
        """
        query = """
            SELECT * FROM courses 
            WHERE DATEDIFF(CURDATE(), week_date) >= 7 
            AND needs_revision = FALSE
            ORDER BY week_date ASC
            LIMIT 10
        """
        return DatabaseManager.execute_query(query, fetch=True)
    
    @staticmethod
    def mark_as_revised(course_id):
        """
        Marque un cours comme ayant été révisé.
        
        Args:
            course_id (int): ID du cours
        """
        query = "UPDATE courses SET needs_revision = TRUE WHERE id = %s"
        DatabaseManager.execute_query(query, (course_id,))
    
    @staticmethod
    def delete_course(course_id):
        """
        Supprime un cours de la base de données.
        
        Args:
            course_id (int): ID du cours à supprimer
        """
        query = "DELETE FROM courses WHERE id = %s"
        DatabaseManager.execute_query(query, (course_id,))
    
    @staticmethod
    def get_courses_by_date(target_date):
        """
        Récupère les cours pour une date spécifique.
        
        Args:
            target_date (date): Date cible
        
        Returns:
            list: Liste des cours pour cette date
        """
        query = """
            SELECT * FROM courses 
            WHERE week_date = %s
            ORDER BY start_time
        """
        return DatabaseManager.execute_query(query, (target_date,), fetch=True)
    
    @staticmethod
    def update_course(course_id, name=None, day_of_week=None, 
                     start_time=None, end_time=None):
        """
        Met à jour les informations d'un cours.
        
        Args:
            course_id (int): ID du cours
            name (str, optional): Nouveau nom
            day_of_week (str, optional): Nouveau jour
            start_time (str, optional): Nouvelle heure de début
            end_time (str, optional): Nouvelle heure de fin
        """
        updates = []
        params = []
        
        if name:
            updates.append("name = %s")
            params.append(name)
        if day_of_week:
            updates.append("day_of_week = %s")
            params.append(day_of_week)
        if start_time:
            updates.append("start_time = %s")
            params.append(start_time)
        if end_time:
            updates.append("end_time = %s")
            params.append(end_time)
        
        if updates:
            params.append(course_id)
            query = f"UPDATE courses SET {', '.join(updates)} WHERE id = %s"
            DatabaseManager.execute_query(query, tuple(params))