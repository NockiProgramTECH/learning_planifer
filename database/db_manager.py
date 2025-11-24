"""Gestionnaire de connexion à la base de données MySQL"""

import pymysql
from contextlib import contextmanager
from config import DB_CONFIG

class DatabaseManager:
    """
    Gère les connexions et opérations avec la base de données MySQL.
    Utilise des context managers pour une gestion sûre des connexions.
    """
    
    @staticmethod
    @contextmanager
    def get_connection():
        """
        Context manager pour gérer automatiquement les connexions MySQL.
        Gère commit/rollback automatiquement.
        
        Utilisation:
            with DatabaseManager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        conn = None
        try:
            conn = pymysql.connect(**DB_CONFIG)
            yield conn
            conn.commit()
        except pymysql.Error as e:
            if conn:
                conn.rollback()
            raise Exception(f"Erreur base de données: {e}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """
        Exécute une requête SQL avec paramètres.
        
        Args:
            query (str): Requête SQL à exécuter
            params (tuple): Paramètres de la requête (optionnel)
            fetch (bool): Si True, retourne les résultats (SELECT)
        
        Returns:
            list: Résultats si fetch=True
            int: ID de la dernière ligne insérée si fetch=False
        """
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, params or ())
            
            if fetch:
                return cursor.fetchall()
            return cursor.lastrowid
    
    @staticmethod
    def execute_many(query, params_list):
        """
        Exécute plusieurs requêtes identiques en batch (optimisé).
        
        Args:
            query (str): Requête SQL avec placeholders
            params_list (list): Liste de tuples de paramètres
        
        Returns:
            int: Nombre de lignes affectées
        """
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            return cursor.rowcount
    
    @staticmethod
    def test_connection():
        """
        Teste la connexion à la base de données.
        
        Returns:
            bool: True si la connexion réussit
        """
        try:
            with DatabaseManager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                return True
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False
    
    @staticmethod
    def initialize_database():
        """
        Initialise la base de données avec les matières par défaut.
        À appeler au premier lancement.
        """
        from config import LEARNING_SUBJECTS
        
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier si les matières existent déjà
            cursor.execute("SELECT COUNT(*) as count FROM learning_subjects")
            result = cursor.fetchone()
            
            if result[0] == 0:
                # Insérer les matières par défaut
                query = "INSERT INTO learning_subjects (name, priority) VALUES (%s, 1)"
                for subject in LEARNING_SUBJECTS:
                    cursor.execute(query, (subject,))
                print(f"✅ {len(LEARNING_SUBJECTS)} matières initialisées")