"""Interface de gestion des devoirs"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from models.homework import Homework

class HomeworkManager(ctk.CTkFrame):
    """
    Interface pour gérer les devoirs.
    Permet d'ajouter, visualiser et gérer les devoirs avec leurs échéances.
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Titre
        title = ctk.CTkLabel(
            self,
            text="✏️ Gestion des Devoirs",
            font=("Arial", 28, "bold")
        )
        title.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Frame pour le formulaire
        self.create_form()
        
        # Frame pour la liste
        self.create_list()
        
        # Charger les devoirs existants
        self.load_homework()
    
    def create_form(self):
        """Crée le formulaire d'ajout de devoir"""
        form_frame = ctk.CTkFrame(self, corner_radius=15)
        form_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Titre du formulaire
        ctk.CTkLabel(
            form_frame,
            text="➕ Ajouter un nouveau devoir",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=(15, 20), padx=20, sticky="w")
        
        # Ligne 1: Matière
        ctk.CTkLabel(
            form_frame,
            text="Matière:",
            font=("Arial", 14)
        ).grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.subject_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ex: Technologie IP",
            height=40,
            font=("Arial", 13)
        )
        self.subject_entry.grid(row=1, column=1, columnspan=2, padx=(0, 20), pady=10, sticky="ew")
        
        # Ligne 2: Description
        ctk.CTkLabel(
            form_frame,
            text="Description:",
            font=("Arial", 14)
        ).grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
        
        self.description_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Description du devoir (optionnel)",
            height=40,
            font=("Arial", 13)
        )
        self.description_entry.grid(row=2, column=1, columnspan=2, padx=(0, 20), pady=10, sticky="ew")
        
        # Ligne 3: Date et heure limite
        date_time_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_time_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        date_time_frame.grid_columnconfigure((1, 3), weight=1)
        
        ctk.CTkLabel(
            date_time_frame,
            text="Date limite:",
            font=("Arial", 14)
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.due_date_entry = ctk.CTkEntry(
            date_time_frame,
            placeholder_text="YYYY-MM-DD",
            height=40,
            font=("Arial", 13)
        )
        self.due_date_entry.grid(row=0, column=1, padx=(0, 20), sticky="ew")
        
        # Pré-remplir avec une date dans 7 jours
        future_date = datetime.now().date() + timedelta(days=7)
        self.due_date_entry.insert(0, future_date.strftime("%Y-%m-%d"))
        
        ctk.CTkLabel(
            date_time_frame,
            text="Heure limite:",
            font=("Arial", 14)
        ).grid(row=0, column=2, padx=(0, 10), sticky="w")
        
        self.due_time_entry = ctk.CTkEntry(
            date_time_frame,
            placeholder_text="HH:MM",
            height=40,
            font=("Arial", 13)
        )
        self.due_time_entry.grid(row=0, column=3, sticky="ew")
        self.due_time_entry.insert(0, "18:00")
        
        # Ligne 4: Jours de préparation
        prep_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        prep_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        prep_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            prep_frame,
            text="Jours de préparation:",
            font=("Arial", 14)
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.prep_days_entry = ctk.CTkEntry(
            prep_frame,
            placeholder_text="3",
            height=40,
            font=("Arial", 13),
            width=100
        )
        self.prep_days_entry.grid(row=0, column=1, sticky="w")
        self.prep_days_entry.insert(0, "3")
        
        ctk.CTkLabel(
            prep_frame,
            text="ℹ️ Nombre de jours avant la date limite pour commencer la préparation",
            font=("Arial", 11),
            text_color="gray"
        ).grid(row=0, column=2, sticky="w", padx=20)
        
        # Ligne 5: Boutons
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=3, pady=20, padx=20)
        
        ctk.CTkButton(
            btn_frame,
            text="➕ Ajouter le devoir",
            command=self.add_homework,
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            corner_radius=10
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Actualiser la liste",
            command=self.load_homework,
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
        """Crée la zone d'affichage de la liste des devoirs"""
        list_frame = ctk.CTkFrame(self, corner_radius=15)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            list_frame,
            text="📋 Devoirs à venir",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, pady=(15, 10), padx=20, sticky="w")
        
        self.homework_text = ctk.CTkTextbox(
            list_frame,
            font=("Consolas", 12),
            wrap="word"
        )
        self.homework_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
    
    def clear_form(self):
        """Efface le formulaire"""
        self.subject_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        # Ne pas effacer les dates, juste réinitialiser
        future_date = datetime.now().date() + timedelta(days=7)
        self.due_date_entry.delete(0, 'end')
        self.due_date_entry.insert(0, future_date.strftime("%Y-%m-%d"))
        self.due_time_entry.delete(0, 'end')
        self.due_time_entry.insert(0, "18:00")
        self.subject_entry.focus()
    
    def add_homework(self):
        """Ajoute un nouveau devoir dans la base de données"""
        try:
            # Récupérer les valeurs
            subject = self.subject_entry.get().strip()
            description = self.description_entry.get().strip()
            due_date = self.due_date_entry.get().strip()
            due_time = self.due_time_entry.get().strip()
            prep_days_str = self.prep_days_entry.get().strip()
            
            # Validation
            if not all([subject, due_date, due_time]):
                messagebox.showwarning(
                    "Champs manquants",
                    "Veuillez remplir au minimum: Matière, Date limite et Heure limite"
                )
                return
            
            # Valider et convertir prep_days
            try:
                prep_days = int(prep_days_str)
                if prep_days < 1 or prep_days > 30:
                    raise ValueError("Doit être entre 1 et 30")
            except ValueError:
                messagebox.showerror(
                    "Valeur invalide",
                    "Les jours de préparation doivent être un nombre entre 1 et 30"
                )
                return
            
            # Valider le format de la date
            try:
                date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
                # Vérifier que la date n'est pas dans le passé
                if date_obj < datetime.now().date():
                    messagebox.showwarning(
                        "Date invalide",
                        "La date limite ne peut pas être dans le passé"
                    )
                    return
            except ValueError:
                messagebox.showerror(
                    "Format invalide",
                    "Format de date invalide. Utilisez YYYY-MM-DD (ex: 2024-03-25)"
                )
                return
            
            # Valider le format de l'heure
            try:
                datetime.strptime(due_time, "%H:%M")
            except ValueError:
                messagebox.showerror(
                    "Format invalide",
                    "Format d'heure invalide. Utilisez HH:MM (ex: 18:00)"
                )
                return
            
            # Ajouter dans la base de données
            Homework.add_homework(
                subject, 
                description if description else "Pas de description",
                due_date, 
                due_time, 
                prep_days
            )
            
            messagebox.showinfo(
                "✅ Succès",
                f"Le devoir '{subject}' a été ajouté avec succès!\n\n"
                f"📅 Date limite: {due_date} à {due_time}\n"
                f"⏰ Préparation: {prep_days} jours avant"
            )
            
            # Réinitialiser le formulaire
            self.clear_form()
            
            # Recharger la liste
            self.load_homework()
            
        except Exception as e:
            messagebox.showerror(
                "❌ Erreur",
                f"Erreur lors de l'ajout du devoir:\n\n{str(e)}"
            )
    
    def load_homework(self):
        """Charge et affiche les devoirs"""
        try:
            homework_list = Homework.get_pending_homework()
            
            # Effacer le contenu actuel
            self.homework_text.delete("1.0", "end")
            
            if not homework_list:
                self.homework_text.insert(
                    "1.0",
                    "📭 Aucun devoir en cours.\n\n"
                    "Ajoutez vos devoirs en utilisant le formulaire ci-dessus."
                )
                return
            
            # Afficher les devoirs
            output = "📝 DEVOIRS À VENIR\n"
            output += "=" * 90 + "\n\n"
            
            today = datetime.now().date()
            
            for hw in homework_list:
                # Gérer le type de due_date (peut être date ou str)
                due_date = hw['due_date']
                if isinstance(due_date, str):
                    due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                
                days_left = (due_date - today).days
                
                # Déterminer l'urgence
                if days_left < 0:
                    urgency = "🔴 EN RETARD"
                    urgency_color = "red"
                elif days_left == 0:
                    urgency = "🔴 AUJOURD'HUI"
                    urgency_color = "red"
                elif days_left <= 3:
                    urgency = "🟠 URGENT"
                    urgency_color = "orange"
                elif days_left <= 7:
                    urgency = "🟡 À FAIRE BIENTÔT"
                    urgency_color = "yellow"
                else:
                    urgency = "🟢 OK"
                    urgency_color = "green"
                
                # Formater l'heure
                due_time = hw['due_time']
                if hasattr(due_time, 'strftime'):
                    due_time = due_time.strftime("%H:%M")
                
                output += f"{urgency} | {hw['subject']}\n"
                output += f"  📅 Date limite: {due_date.strftime('%d/%m/%Y')} à {due_time}\n"
                output += f"  ⏳ Temps restant: {days_left} jour(s)\n"
                output += f"  📝 Description: {hw['description']}\n"
                output += f"  🔧 Préparation: Commencer {hw['preparation_days']} jours avant\n"
                output += f"  📊 Statut: {hw['status'].upper()}\n"
                output += "-" * 90 + "\n\n"
            
            output += f"📊 Total: {len(homework_list)} devoirs en cours\n"
            
            # # Statistiques rapides
            urgent_count=sum(1 for hw in homework_list
                             if (isinstance(hw['due_date'], str) and
                                 (datetime.strptime(hw['due_date'], '%Y-%m-%d').date() - today).days <=3) or
                                (not isinstance(hw['due_date'], str) and
                                 (hw['due_date'] - today).days <=3))
                            
            
           
            if urgent_count > 0:
                output += f"⚠️  {urgent_count} devoir(s) urgent(s) (≤3 jours)\n"
            
            self.homework_text.insert("1.0", output)
            
        except Exception as e:
            self.homework_text.delete("1.0", "end")
            self.homework_text.insert(
                "1.0",
                f"❌ Erreur lors du chargement des devoirs:\n\n{str(e)}"
            )
             