"""Interface de gestion des cours"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from models.course import Course

class CourseManager(ctk.CTkFrame):
    """
    Interface pour gérer les cours de la semaine.
    Permet d'ajouter, visualiser et supprimer des cours.
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Titre
        title = ctk.CTkLabel(
            self,
            text="📅 Gestion des Cours",
            font=("Arial", 28, "bold")
        )
        title.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Frame pour le formulaire
        self.create_form()
        
        # Frame pour la liste
        self.create_list()
        
        # Charger les cours existants
        self.load_courses()
    
    def create_form(self):
        """Crée le formulaire d'ajout de cours"""
        form_frame = ctk.CTkFrame(self, corner_radius=15)
        form_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Titre du formulaire
        ctk.CTkLabel(
            form_frame,
            text="➕ Ajouter un nouveau cours",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=(15, 20), padx=20, sticky="w")
        
        # Ligne 1: Nom du cours
        ctk.CTkLabel(
            form_frame,
            text="Nom du cours:",
            font=("Arial", 14)
        ).grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Architecture des Ordinateurs",
            height=40,
            font=("Arial", 13)
        )
        self.name_entry.grid(row=1, column=1, columnspan=2, padx=(0, 20), pady=10, sticky="ew")
        
        # Ligne 2: Jour et Date
        ctk.CTkLabel(
            form_frame,
            text="Jour de la semaine:",
            font=("Arial", 14)
        ).grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.day_combo = ctk.CTkComboBox(
            form_frame,
            values=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"],
            height=40,
            font=("Arial", 13)
        )
        self.day_combo.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.day_combo.set("Lundi")
        
        ctk.CTkLabel(
            form_frame,
            text="Date (semaine du):",
            font=("Arial", 14)
        ).grid(row=2, column=2, padx=(10, 10), pady=10, sticky="w")
        
        # Ligne 3: Date entry
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        date_frame.grid_columnconfigure(1, weight=1)
        
        self.date_entry = ctk.CTkEntry(
            date_frame,
            placeholder_text="YYYY-MM-DD",
            height=40,
            font=("Arial", 13)
        )
        self.date_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Pré-remplir avec le lundi prochain
        today = datetime.now().date()
        days_until_monday = (7 - today.weekday()) % 7
        next_monday = today + timedelta(days=days_until_monday if days_until_monday > 0 else 7)
        self.date_entry.insert(0, next_monday.strftime("%Y-%m-%d"))
        
        ctk.CTkLabel(
            date_frame,
            text="ℹ️ Date du lundi de la semaine",
            font=("Arial", 11),
            text_color="gray"
        ).grid(row=0, column=1, sticky="w", padx=10)
        
        # Ligne 4: Horaires
        time_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        time_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        time_frame.grid_columnconfigure((1, 3), weight=1)
        
        ctk.CTkLabel(
            time_frame,
            text="Heure de début:",
            font=("Arial", 14)
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.start_time_entry = ctk.CTkEntry(
            time_frame,
            placeholder_text="Ex: 14:00",
            height=40,
            font=("Arial", 13)
        )
        self.start_time_entry.grid(row=0, column=1, padx=(0, 20), sticky="ew")
        
        ctk.CTkLabel(
            time_frame,
            text="Heure de fin:",
            font=("Arial", 14)
        ).grid(row=0, column=2, padx=(0, 10), sticky="w")
        
        self.end_time_entry = ctk.CTkEntry(
            time_frame,
            placeholder_text="Ex: 18:00",
            height=40,
            font=("Arial", 13)
        )
        self.end_time_entry.grid(row=0, column=3, sticky="ew")
        
        # Ligne 5: Boutons
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=3, pady=20, padx=20)
        
        ctk.CTkButton(
            btn_frame,
            text="➕ Ajouter le cours",
            command=self.add_course,
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            corner_radius=10
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Actualiser la liste",
            command=self.load_courses,
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            corner_radius=10,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Effacer le formulaire",
            command=self.clear_form,
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            corner_radius=10,
            fg_color="orange",
            hover_color="darkorange"
        ).pack(side="left", padx=10)
    
    def create_list(self):
        """Crée la zone d'affichage de la liste des cours"""
        list_frame = ctk.CTkFrame(self, corner_radius=15)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            list_frame,
            text="📋 Cours de la semaine",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, pady=(15, 10), padx=20, sticky="w")
        
        self.courses_text = ctk.CTkTextbox(
            list_frame,
            font=("Consolas", 12),
            wrap="word"
        )
        self.courses_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
    
    def clear_form(self):
        """Efface le formulaire"""
        self.name_entry.delete(0, 'end')
        self.start_time_entry.delete(0, 'end')
        self.end_time_entry.delete(0, 'end')
        self.name_entry.focus()
    
    def add_course(self):
        """Ajoute un nouveau cours dans la base de données"""
        try:
            # Récupérer les valeurs
            name = self.name_entry.get().strip()
            day = self.day_combo.get()
            start_time = self.start_time_entry.get().strip()
            end_time = self.end_time_entry.get().strip()
            week_date = self.date_entry.get().strip()
            
            # Validation
            if not all([name, day, start_time, end_time, week_date]):
                messagebox.showwarning(
                    "Champs manquants",
                    "Veuillez remplir tous les champs"
                )
                return
            
            # Valider le format des heures
            try:
                datetime.strptime(start_time, "%H:%M")
                datetime.strptime(end_time, "%H:%M")
            except ValueError:
                messagebox.showerror(
                    "Format invalide",
                    "Format d'heure invalide. Utilisez HH:MM (ex: 14:00)"
                )
                return
            
            # Valider la date
            try:
                datetime.strptime(week_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Format invalide",
                    "Format de date invalide. Utilisez YYYY-MM-DD (ex: 2024-03-25)"
                )
                return
            
            # Ajouter dans la base de données
            Course.add_course(name, day, start_time, end_time, week_date)
            
            messagebox.showinfo(
                "✅ Succès",
                f"Le cours '{name}' a été ajouté avec succès!"
            )
            
            # Réinitialiser le formulaire
            self.clear_form()
            
            # Recharger la liste
            self.load_courses()
            
        except Exception as e:
            messagebox.showerror(
                "❌ Erreur",
                f"Erreur lors de l'ajout du cours:\n\n{str(e)}"
            )
    
    def load_courses(self):
        """Charge et affiche les cours de la semaine"""
        try:
            week_date = self.date_entry.get().strip()
            week_start = datetime.strptime(week_date, "%Y-%m-%d").date()
            
            courses = Course.get_courses_by_week(week_start)
            
            # Effacer le contenu actuel
            self.courses_text.delete("1.0", "end")
            
            if not courses:
                self.courses_text.insert(
                    "1.0",
                    "📭 Aucun cours pour cette semaine.\n\n"
                    "Ajoutez vos cours en utilisant le formulaire ci-dessus."
                )
                return
            
            # Afficher les cours
            output = f"📅 COURS DE LA SEMAINE DU {week_start.strftime('%d/%m/%Y')}\n"
            output += "=" * 80 + "\n\n"
            
            # Grouper par jour
            days_order = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            courses_by_day = {day: [] for day in days_order}
            
            for course in courses:
                day = course['day_of_week']
                if day in courses_by_day:
                    courses_by_day[day].append(course)
            
            # Afficher par jour
            for day in days_order:
                day_courses = courses_by_day[day]
                if day_courses:
                    output += f"\n📌 {day.upper()}\n"
                    output += "-" * 80 + "\n"
                    
                    for course in day_courses:
                        start = course['start_time']
                        end = course['end_time']
                        
                        # Convertir en string HH:MM (gérer time, timedelta, str)
                        if hasattr(start, 'total_seconds'):  # timedelta
                            total_seconds = int(start.total_seconds())
                            start = f"{(total_seconds // 3600):02d}:{((total_seconds % 3600) // 60):02d}"
                        elif hasattr(start, 'strftime'):  # time
                            start = start.strftime("%H:%M")
                        else:
                            start = str(start)
                        
                        if hasattr(end, 'total_seconds'):  # timedelta
                            total_seconds = int(end.total_seconds())
                            end = f"{(total_seconds // 3600):02d}:{((total_seconds % 3600) // 60):02d}"
                        elif hasattr(end, 'strftime'):  # time
                            end = end.strftime("%H:%M")
                        else:
                            end = str(end)
                        
                        output += f"  🎓 {course['name']}\n"
                        output += f"     ⏰ {start} - {end}\n"
                        output += f"     📅 {course['week_date']}\n\n"
            
            output += "\n" + "=" * 80 + "\n"
            output += f"📊 Total: {len(courses)} cours cette semaine\n"
            
            self.courses_text.insert("1.0", output)
            
        except ValueError:
            self.courses_text.delete("1.0", "end")
            self.courses_text.insert(
                "1.0",
                "❌ Format de date invalide.\n\n"
                "Utilisez le format YYYY-MM-DD (ex: 2024-03-25)"
            )
        except Exception as e:
            self.courses_text.delete("1.0", "end")
            self.courses_text.insert(
                "1.0",
                f"❌ Erreur lors du chargement des cours:\n\n{str(e)}"
            )