"""Visualisation du planning de la semaine"""

import customtkinter as ctk
from datetime import datetime, timedelta
from database.db_manager import DatabaseManager
from services.scheduler import Scheduler

class ScheduleViewer(ctk.CTkFrame):
    """
    Affichage détaillé du planning hebdomadaire.
    Permet de naviguer entre les semaines et voir toutes les activités.
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Calculer le lundi de la semaine prochaine par défaut
        today = datetime.now().date()
        days_until_monday = (7 - today.weekday()) % 7
        self.current_week_start = today + timedelta(
            days=days_until_monday if days_until_monday > 0 else 7
        )
        
        # Titre
        self.title_label = ctk.CTkLabel(
            self,
            text="📊 Planning de la Semaine",
            font=("Arial", 28, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Contrôles de navigation
        self.create_controls()
        
        # Zone d'affichage
        self.create_display_area()
        
        # Charger le planning
        self.load_schedule()
    
    def create_controls(self):
        """Crée les contrôles de navigation"""
        controls_frame = ctk.CTkFrame(self, corner_radius=15)
        controls_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Label de la semaine courante
        self.week_label = ctk.CTkLabel(
            controls_frame,
            text=f"Semaine du {self.current_week_start.strftime('%d/%m/%Y')}",
            font=("Arial", 18, "bold")
        )
        self.week_label.grid(row=0, column=1, padx=20, pady=15)
        
        # Boutons de navigation
        btn_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        ctk.CTkButton(
            btn_frame,
            text="◀◀ Semaine précédente",
            command=self.previous_week,
            width=180,
            height=40,
            font=("Arial", 13, "bold"),
            corner_radius=10
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📅 Aujourd'hui",
            command=self.go_to_current_week,
            width=140,
            height=40,
            font=("Arial", 13, "bold"),
            corner_radius=10,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="left", padx=5)
        
        # Boutons à droite
        btn_frame_right = ctk.CTkFrame(controls_frame, fg_color="transparent")
        btn_frame_right.grid(row=0, column=2, padx=20, pady=15, sticky="e")
        
        ctk.CTkButton(
            btn_frame_right,
            text="Semaine suivante ▶▶",
            command=self.next_week,
            width=180,
            height=40,
            font=("Arial", 13, "bold"),
            corner_radius=10
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame_right,
            text="🔄 Actualiser",
            command=self.load_schedule,
            width=140,
            height=40,
            font=("Arial", 13, "bold"),
            corner_radius=10,
            fg_color="green",
            hover_color="darkgreen"
        ).pack(side="left", padx=5)
        
        # Statistiques de la semaine
        self.stats_label = ctk.CTkLabel(
            controls_frame,
            text="",
            font=("Arial", 12),
            text_color="gray"
        )
        self.stats_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
    
    def create_display_area(self):
        """Crée la zone d'affichage du planning"""
        display_frame = ctk.CTkFrame(self, corner_radius=15)
        display_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_rowconfigure(0, weight=1)
        
        # Textbox avec scrollbar
        self.schedule_text = ctk.CTkTextbox(
            display_frame,
            font=("Consolas", 11),
            wrap="word"
        )
        self.schedule_text.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def previous_week(self):
        """Navigue vers la semaine précédente"""
        self.current_week_start -= timedelta(days=7)
        self.update_week_label()
        self.load_schedule()
    
    def next_week(self):
        """Navigue vers la semaine suivante"""
        self.current_week_start += timedelta(days=7)
        self.update_week_label()
        self.load_schedule()
    
    def go_to_current_week(self):
        """Revient à la semaine courante"""
        today = datetime.now().date()
        days_until_monday = (7 - today.weekday()) % 7
        self.current_week_start = today + timedelta(
            days=days_until_monday if days_until_monday > 0 else 7
        )
        self.update_week_label()
        self.load_schedule()
    
    def update_week_label(self):
        """Met à jour le label de la semaine"""
        week_end = self.current_week_start + timedelta(days=6)
        self.week_label.configure(
            text=f"Semaine du {self.current_week_start.strftime('%d/%m/%Y')} "
                 f"au {week_end.strftime('%d/%m/%Y')}"
        )
    
    def load_schedule(self):
        """Charge et affiche le planning de la semaine"""
        try:
            # Récupérer les activités de la semaine
            query = """
                SELECT * FROM schedule_slots
                WHERE date >= %s AND date < DATE_ADD(%s, INTERVAL 7 DAY)
                ORDER BY date, start_time
            """
            activities = DatabaseManager.execute_query(
                query,
                (self.current_week_start, self.current_week_start),
                fetch=True
            )
            
            # Effacer le contenu actuel
            self.schedule_text.delete("1.0", "end")
            
            if not activities:
                self.schedule_text.insert(
                    "1.0",
                    "📭 Aucune activité planifiée pour cette semaine.\n\n"
                    "Pour générer un planning:\n"
                    "1. Ajoutez vos cours dans 'Gestion des Cours'\n"
                    "2. Ajoutez vos devoirs dans 'Gestion des Devoirs'\n"
                    "3. Cliquez sur 'Générer Planning' dans le menu"
                )
                self.stats_label.configure(text="")
                return
            
            # Organiser par jour
            days_data = {}
            for activity in activities:
                date = activity['date']
                if isinstance(date, str):
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                
                date_str = date.strftime('%Y-%m-%d')
                if date_str not in days_data:
                    days_data[date_str] = []
                days_data[date_str].append(activity)
            
            # Générer l'affichage
            output = self._generate_schedule_display(days_data, activities)
            self.schedule_text.insert("1.0", output)
            
            # Mettre à jour les statistiques
            self._update_statistics(activities)
            
        except Exception as e:
            self.schedule_text.delete("1.0", "end")
            self.schedule_text.insert(
                "1.0",
                f"❌ Erreur lors du chargement du planning:\n\n{str(e)}"
            )
            self.stats_label.configure(text="")
    
    def _generate_schedule_display(self, days_data, activities):
        """
        Génère l'affichage formaté du planning.
        
        Args:
            days_data (dict): Données organisées par jour
            activities (list): Liste complète des activités
        
        Returns:
            str: Texte formaté pour l'affichage
        """
        week_end = self.current_week_start + timedelta(days=6)
        output = f"📅 PLANNING DÉTAILLÉ DE LA SEMAINE\n"
        output += f"Du {self.current_week_start.strftime('%d/%m/%Y')} "
        output += f"au {week_end.strftime('%d/%m/%Y')}\n"
        output += "=" * 100 + "\n\n"
        
        days_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        
        # Icônes selon le type d'activité
        icons = {
            'course': '🎓',
            'homework': '✏️',
            'learning': '📚',
            'revision': '🔄'
        }
        
        # Labels pour les types d'activités
        type_labels = {
            'course': 'COURS',
            'homework': 'DEVOIR',
            'learning': 'APPRENTISSAGE',
            'revision': 'RÉVISION'
        }
        
        # Afficher jour par jour
        for i in range(7):
            current_date = self.current_week_start + timedelta(days=i)
            date_str = current_date.strftime('%Y-%m-%d')
            day_name = days_names[i]
            
            # En-tête du jour
            output += "\n" + "=" * 100 + "\n"
            output += f"📌 {day_name.upper()} - {current_date.strftime('%d/%m/%Y')}\n"
            output += "=" * 100 + "\n\n"
            
            if date_str in days_data:
                for activity in days_data[date_str]:
                    # Icône et type
                    icon = icons.get(activity['activity_type'], '📌')
                    type_label = type_labels.get(activity['activity_type'], 'ACTIVITÉ')
                    
                    # Horaires - Gérer tous les types (time, timedelta, str)
                    start = activity['start_time']
                    end = activity['end_time']
                    
                    # Convertir en string HH:MM
                    if hasattr(start, 'total_seconds'):  # timedelta
                        total_seconds = int(start.total_seconds())
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        start = f"{hours:02d}:{minutes:02d}"
                    elif hasattr(start, 'strftime'):  # time
                        start = start.strftime("%H:%M")
                    else:  # str
                        start = str(start)
                    
                    if hasattr(end, 'total_seconds'):  # timedelta
                        total_seconds = int(end.total_seconds())
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        end = f"{hours:02d}:{minutes:02d}"
                    elif hasattr(end, 'strftime'):  # time
                        end = end.strftime("%H:%M")
                    else:  # str
                        end = str(end)
                    
                    # Calculer la durée
                    try:
                        # Convertir en minutes
                        start_minutes = int(start.split(':')[0]) * 60 + int(start.split(':')[1])
                        end_minutes = int(end.split(':')[0]) * 60 + int(end.split(':')[1])
                        duration = end_minutes - start_minutes
                        
                    except:
                        duration = 90  # Valeur par défaut
                    hours = duration // 60
                    mins = duration % 60
                    duration_str = f"{hours}h{mins:02d}" if hours > 0 else f"{mins}min"
                    
                    # Afficher l'activité
                    output += f"{icon} [{type_label}] {start} - {end} ({duration_str})\n"
                    output += f"   📋 {activity['subject']}\n"
                    if activity['description']:
                        output += f"   💬 {activity['description']}\n"
                    output += "\n"
            else:
                output += "   💤 Journée libre - Aucune activité planifiée\n\n"
        
        # Footer
        output += "\n" + "=" * 100 + "\n"
        output += "💡 RAPPELS:\n"
        output += "   • Les notifications vous alertent 15 minutes avant chaque activité\n"
        output += "   • Prenez des pauses régulières de 15 minutes\n"
        output += "   • Restez hydraté et bien reposé pour un apprentissage optimal\n"
        output += "=" * 100 + "\n"
        
        return output
    
    def _update_statistics(self, activities):
        """
        Met à jour les statistiques affichées.
        
        Args:
            activities (list): Liste des activités de la semaine
        """
        # Compter par type
        counts = {
            'course': 0,
            'homework': 0,
            'learning': 0,
            'revision': 0
        }
        
        total_minutes = 0
        
        for activity in activities:
            activity_type = activity['activity_type']
            counts[activity_type] = counts.get(activity_type, 0) + 1
            
            # Calculer la durée
            start = activity['start_time']
            end = activity['end_time']
            
            if hasattr(start, 'strftime'):
                start = start.strftime("%H:%M")
            if hasattr(end, 'strftime'):
                end = end.strftime("%H:%M")
            
            start_minutes = int(start.split(':')[0]) * 60 + int(start.split(':')[1])
            end_minutes = int(end.split(':')[0]) * 60 + int(end.split(':')[1])
            total_minutes += (end_minutes - start_minutes)
        
        total_hours = total_minutes / 60
        
        # Construire le texte des statistiques
        stats_parts = []
        if counts['course'] > 0:
            stats_parts.append(f"🎓 {counts['course']} cours")
        if counts['homework'] > 0:
            stats_parts.append(f"✏️ {counts['homework']} devoirs")
        if counts['learning'] > 0:
            stats_parts.append(f"📚 {counts['learning']} sessions d'apprentissage")
        if counts['revision'] > 0:
            stats_parts.append(f"🔄 {counts['revision']} révisions")
        
        stats_text = " • ".join(stats_parts)
        stats_text += f" • ⏱️ Total: {total_hours:.1f}h ({len(activities)} activités)"
        
        self.stats_label.configure(text=stats_text)