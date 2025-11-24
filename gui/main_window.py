"""Fenêtre principale de l'application avec menu de navigation"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from gui.course_manager import CourseManager
from gui.homework_manager import HomeworkManager
from gui.schedule_viewer import ScheduleViewer
from services.scheduler import Scheduler
from models.homework import Homework
from models.learning import LearningSubject

class MainWindow(ctk.CTk):
    """
    Fenêtre principale de l'application Learning Planner.
    Contient le menu de navigation et gère les différentes vues.
    """
    
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title("📚 Planificateur d'Apprentissage Intelligent")
        self.geometry("1400x900")
        
        # Centrer la fenêtre
        self.center_window()
        
        # Configuration de la grille
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Variables
        self.current_view = None
        
        # Créer l'interface
        self.create_sidebar()
        self.create_content_frame()
        
        # Afficher l'accueil par défaut
        self.show_home()
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_sidebar(self):
        """Crée le menu latéral avec les boutons de navigation"""
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_rowconfigure(8, weight=1)
        
        # Logo/Titre avec gradient
        title_frame = ctk.CTkFrame(self.sidebar, fg_color=("#3b82f6", "#2563eb"))
        title_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        title = ctk.CTkLabel(
            title_frame,
            text="📚 Learning\nPlanner",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        title.pack(pady=30)
        
        # Séparateur
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="gray")
        separator.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Boutons de navigation
        self.nav_buttons = []
        
        buttons_config = [
            ("🏠 Accueil", self.show_home, 2),
            ("📅 Gestion des Cours", self.show_courses, 3),
            ("✏️ Gestion des Devoirs", self.show_homework, 4),
            ("📊 Planning Semaine", self.show_schedule, 5),
            ("🔄 Générer Planning", self.generate_schedule, 6),
            ("📈 Statistiques", self.show_statistics, 7),
        ]
        
        for text, command, row in buttons_config:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=45,
                corner_radius=10,
                font=("Arial", 14, "bold"),
                fg_color="transparent",
                hover_color=("#e0e0e0", "#404040"),
                anchor="w",
                text_color=("gray10", "gray90")
            )
            btn.grid(row=row, column=0, padx=15, pady=8, sticky="ew")
            self.nav_buttons.append(btn)
        
        # Espace flexible
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.grid(row=8, column=0, sticky="nsew")
        
        # Informations en bas
        info_frame = ctk.CTkFrame(self.sidebar)
        info_frame.grid(row=9, column=0, sticky="ew", padx=15, pady=10)
        
        version_label = ctk.CTkLabel(
            info_frame,
            text="Version 1.0\n© 2024",
            font=("Arial", 10),
            text_color="gray"
        )
        version_label.pack(pady=5)
    
    def create_content_frame(self):
        """Crée la zone principale de contenu"""
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def highlight_button(self, active_button):
        """
        Met en évidence le bouton actif dans le menu.
        
        Args:
            active_button (int): Index du bouton actif
        """
        for i, btn in enumerate(self.nav_buttons):
            if i == active_button:
                btn.configure(fg_color=("#3b82f6", "#2563eb"))
            else:
                btn.configure(fg_color="transparent")
    
    def clear_content(self):
        """Efface le contenu actuel de la zone principale"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """Affiche l'écran d'accueil avec les statistiques"""
        self.clear_content()
        self.highlight_button(0)
        
        # Container principal
        container = ctk.CTkFrame(self.content_frame)
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1)
        
        # En-tête
        header = ctk.CTkFrame(container, fg_color=("#3b82f6", "#2563eb"))
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 20))
        
        title = ctk.CTkLabel(
            header,
            text="🎓 Bienvenue dans votre Planificateur d'Apprentissage",
            font=("Arial", 32, "bold"),
            text_color="white"
        )
        title.pack(pady=30)
        
        # Statistiques rapides
        stats_frame = ctk.CTkFrame(container)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 20))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        try:
            # Récupérer les statistiques
            homework_stats = Homework.get_statistics()
            learning_stats = LearningSubject.get_statistics()
            
            stats_data = [
                ("📚 Matières", str(learning_stats.get('total_subjects', 8)), "à apprendre"),
                ("⏱️ Heures totales", f"{learning_stats.get('total_hours', 0):.1f}h", "d'apprentissage"),
                ("✏️ Devoirs actifs", str(homework_stats.get('pending', 0) + homework_stats.get('in_progress', 0)), "en cours"),
                ("🔴 Devoirs urgents", str(homework_stats.get('overdue', 0)), "en retard")
            ]
        except:
            stats_data = [
                ("📚 Matières", "8", "à apprendre"),
                ("⏱️ Heures totales", "0.0h", "d'apprentissage"),
                ("✏️ Devoirs actifs", "0", "en cours"),
                ("🔴 Devoirs urgents", "0", "en retard")
            ]
        
        for i, (label, value, subtitle) in enumerate(stats_data):
            stat_card = ctk.CTkFrame(stats_frame, corner_radius=15)
            stat_card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Arial", 16, "bold")
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                stat_card,
                text=value,
                font=("Arial", 36, "bold"),
                text_color=("#3b82f6", "#60a5fa")
            ).pack(pady=5)
            
            ctk.CTkLabel(
                stat_card,
                text=subtitle,
                font=("Arial", 12),
                text_color="gray"
            ).pack(pady=(5, 20))
        
        # Guide d'utilisation
        guide_frame = ctk.CTkFrame(container)
        guide_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        guide_frame.grid_columnconfigure(0, weight=1)
        guide_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            guide_frame,
            text="📌 Guide d'utilisation",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        guide_text = """
🎯 COMMENT UTILISER LE PLANIFICATEUR

📅 Chaque samedi (pour la semaine suivante):
   1. Ouvrez "Gestion des Cours"
   2. Ajoutez tous vos cours avec horaires précis
   3. Ouvrez "Gestion des Devoirs"
   4. Ajoutez vos devoirs avec dates limites
   5. Cliquez sur "Générer Planning"
   6. Consultez votre planning dans "Planning Semaine"

🔔 Au quotidien:
   • Les notifications vous alertent 15 minutes avant chaque activité
   • Consultez votre planning pour voir vos activités
   • Le système gère automatiquement l'apprentissage des matières

📚 Matières gérées automatiquement:
   ✓ Python               ✓ HTML
   ✓ CSS                  ✓ PHP
   ✓ MySQL                ✓ PostgreSQL
   ✓ Mathématiques        ✓ Lecture de la Bible

⚡ Fonctionnalités intelligentes:
   • Priorisation automatique des devoirs urgents (≤3 jours)
   • Révisions des cours anciens (>7 jours)
   • Répartition équitable des 8 matières
   • Respect des pauses repas (12h-13h, 19h-20h)
   • Créneaux de 1h30 avec pauses de 15 minutes

💡 Astuce: Générez un nouveau planning chaque semaine pour rester organisé!
        """
        
        guide_textbox = ctk.CTkTextbox(
            guide_frame,
            font=("Consolas", 13),
            wrap="word"
        )
        guide_textbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        guide_textbox.insert("1.0", guide_text)
        guide_textbox.configure(state="disabled")
    
    def show_courses(self):
        """Affiche l'interface de gestion des cours"""
        self.clear_content()
        self.highlight_button(1)
        manager = CourseManager(self.content_frame)
        manager.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    def show_homework(self):
        """Affiche l'interface de gestion des devoirs"""
        self.clear_content()
        self.highlight_button(2)
        manager = HomeworkManager(self.content_frame)
        manager.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    def show_schedule(self):
        """Affiche le planning de la semaine"""
        self.clear_content()
        self.highlight_button(3)
        viewer = ScheduleViewer(self.content_frame)
        viewer.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    def generate_schedule(self):
        """Génère le planning de la semaine"""
        self.highlight_button(4)
        
        # Calculer le prochain lundi
        today = datetime.now().date()
        days_until_monday = (7 - today.weekday()) % 7
        next_monday = today + timedelta(days=days_until_monday if days_until_monday > 0 else 7)
        
        # Confirmer avec l'utilisateur
        response = messagebox.askyesno(
            "Générer le planning",
            f"Générer le planning pour la semaine du {next_monday.strftime('%d/%m/%Y')} ?\n\n"
            "Note: L'ancien planning de cette semaine sera remplacé."
        )
        
        if not response:
            return
        
        try:
            # Générer le planning
            count = Scheduler.generate_weekly_schedule(next_monday)
            
            messagebox.showinfo(
                "✅ Succès",
                f"Planning généré avec succès!\n\n"
                f"📅 Semaine du {next_monday.strftime('%d/%m/%Y')}\n"
                f"📊 {count} activités planifiées\n\n"
                "Consultez 'Planning Semaine' pour voir les détails."
            )
            
            # Afficher le planning
            self.show_schedule()
            
        except Exception as e:
            messagebox.showerror(
                "❌ Erreur",
                f"Erreur lors de la génération du planning:\n\n{str(e)}"
            )
    
    def show_statistics(self):
        """Affiche les statistiques détaillées"""
        self.clear_content()
        self.highlight_button(5)
        
        container = ctk.CTkFrame(self.content_frame)
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            container,
            text="📈 Statistiques d'Apprentissage",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)
        
        # Placeholder pour les statistiques
        info = ctk.CTkLabel(
            container,
            text="Statistiques détaillées à venir...",
            font=("Arial", 16)
        )
        info.pack(pady=40)