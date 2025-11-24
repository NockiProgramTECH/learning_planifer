"""
Point d'entrée principal de l'application Learning Planner.
Lance l'interface graphique et les services en arrière-plan.
"""

import sys
import customtkinter as ctk
from tkinter import messagebox
from gui.main_window import MainWindow
from services.notification import NotificationService
from database.db_manager import DatabaseManager

def check_database_connection():
    """
    Vérifie la connexion à la base de données avant de lancer l'application.
    
    Returns:
        bool: True si la connexion réussit, False sinon
    """
    print("🔍 Vérification de la connexion à la base de données...")
    
    try:
        if DatabaseManager.test_connection():
            print("✅ Connexion à la base de données réussie")
            return True
        else:
            print("❌ Impossible de se connecter à la base de données")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def initialize_database():
    """
    Initialise la base de données avec les données par défaut si nécessaire.
    """
    try:
        print("🔧 Initialisation de la base de données...")
        DatabaseManager.initialize_database()
        print("✅ Base de données initialisée")
    except Exception as e:
        print(f"⚠️ Avertissement lors de l'initialisation: {e}")

def main():
    """
    Fonction principale qui lance l'application.
    """
    print("=" * 60)
    print("📚 LEARNING PLANNER - Planificateur d'Apprentissage Intelligent")
    print("=" * 60)
    print()
    
    # Vérifier la connexion à la base de données
    if not check_database_connection():
        messagebox.showerror(
            "Erreur de connexion",
            "Impossible de se connecter à la base de données MySQL.\n\n"
            "Vérifiez que :\n"
            "1. MySQL est installé et démarré\n"
            "2. La base de données 'learning_planner' existe\n"
            "3. Les identifiants dans config.py sont corrects\n\n"
            "Consultez le fichier README pour l'installation."
        )
        sys.exit(1)
    
    # Initialiser la base de données
    initialize_database()
    
    # Configuration de CustomTkinter
    print("🎨 Configuration de l'interface...")
    ctk.set_appearance_mode("dark")  # Modes: "system", "light", "dark"
    ctk.set_default_color_theme("blue")  # Thèmes: "blue", "green", "dark-blue"
    
    print("✅ Interface configurée")
    print()
    
    # Créer la fenêtre principale
    print("🚀 Lancement de l'application...")
    try:
        app = MainWindow()
        
        # Démarrer le service de notifications
        print("🔔 Démarrage du service de notifications...")
        notification_service = NotificationService()
        notification_service.start()
        
        # Tester les notifications
        if notification_service.send_test_notification():
            print("✅ Service de notifications actif")
        else:
            print("⚠️ Les notifications ne fonctionnent pas correctement")
        
        print()
        print("=" * 60)
        print("✅ Application lancée avec succès!")
        print("=" * 60)
        print()
        print("📌 Guide rapide:")
        print("   1. Ajoutez vos cours chaque samedi")
        print("   2. Ajoutez vos devoirs avec dates limites")
        print("   3. Cliquez sur 'Générer Planning'")
        print("   4. Consultez votre planning de la semaine")
        print()
        print("🔔 Les notifications vous alerteront 15 minutes avant chaque activité")
        print()
        print("=" * 60)
        print()
        
        # Lancer la boucle principale de l'interface
        app.mainloop()
        
        # Arrêter les notifications à la fermeture
        print("\n🔕 Arrêt du service de notifications...")
        notification_service.stop()
        
        print("👋 Application fermée. À bientôt!")
        
    except Exception as e:
        print(f"\n❌ Erreur lors du lancement de l'application:")
        print(f"   {str(e)}")
        messagebox.showerror(
            "Erreur",
            f"Une erreur est survenue lors du lancement:\n\n{str(e)}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()