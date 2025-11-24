"""Service de planification intelligente des activités"""

from datetime import datetime, timedelta, time, date
from models.course import Course
from models.homework import Homework
from models.learning import LearningSubject
from database.db_manager import DatabaseManager
from config import PLANNING_CONFIG

class Scheduler:
    """
    Algorithme de planification intelligente.
    Génère automatiquement un planning équilibré pour la semaine.
    """
    
    @staticmethod
    def parse_time(time_str):
        """Convertit une chaîne HH:MM en objet time"""
        return datetime.strptime(time_str, '%H:%M').time()
    
    @staticmethod
    def time_to_minutes(t):
        """Convertit un objet time en minutes depuis minuit"""
        if isinstance(t, str):
            t = Scheduler.parse_time(t)
        return t.hour * 60 + t.minute
    
    @staticmethod
    def minutes_to_time(minutes):
        """Convertit des minutes depuis minuit en objet time"""
        hours = minutes // 60
        mins = minutes % 60
        return time(hour=min(hours, 23), minute=min(mins, 59))
    
    @staticmethod
    def get_day_name(date_obj):
        """Retourne le nom du jour en français"""
        days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        return days[date_obj.weekday()]
    
    @staticmethod
    def get_free_slots(date_obj, courses):
        """
        Calcule les créneaux horaires libres pour une journée donnée.
        
        Args:
            date_obj (date): Date pour laquelle calculer les créneaux
            courses (list): Liste des cours de la semaine
        
        Returns:
            list: Liste de tuples (start_minutes, end_minutes) représentant les créneaux libres
        """
        day_start = Scheduler.time_to_minutes(PLANNING_CONFIG['day_start'])
        day_end = Scheduler.time_to_minutes(PLANNING_CONFIG['day_end'])
        
        # Créneaux occupés
        occupied = []
        
        # Ajouter les cours du jour
        day_name = Scheduler.get_day_name(date_obj)
        for course in courses:
            course_date = course['week_date']
            if isinstance(course_date, str):
                course_date = datetime.strptime(course_date, '%Y-%m-%d').date()
            
            if course_date == date_obj:
                start = Scheduler.time_to_minutes(course['start_time'])
                end = Scheduler.time_to_minutes(course['end_time'])
                occupied.append((start, end))
        
        # Ajouter les pauses repas
        lunch_start = Scheduler.time_to_minutes(PLANNING_CONFIG['lunch_break'][0])
        lunch_end = Scheduler.time_to_minutes(PLANNING_CONFIG['lunch_break'][1])
        occupied.append((lunch_start, lunch_end))
        
        dinner_start = Scheduler.time_to_minutes(PLANNING_CONFIG['dinner_break'][0])
        dinner_end = Scheduler.time_to_minutes(PLANNING_CONFIG['dinner_break'][1])
        occupied.append((dinner_start, dinner_end))
        
        # Trier les créneaux occupés
        occupied.sort()
        
        # Fusionner les créneaux qui se chevauchent
        merged = []
        for start, end in occupied:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        
        # Calculer les créneaux libres
        free_slots = []
        current = day_start
        
        for start, end in merged:
            if current < start:
                free_slots.append((current, start))
            current = max(current, end)
        
        if current < day_end:
            free_slots.append((current, day_end))
        
        return free_slots
    
    @staticmethod
    def generate_weekly_schedule(week_start_date):
        """
        Génère le planning complet pour une semaine.
        
        Algorithme:
        1. Supprimer l'ancien planning de la semaine
        2. Récupérer tous les cours, devoirs et matières
        3. Pour chaque jour:
           - Ajouter les cours
           - Calculer les créneaux libres
           - Allouer dans l'ordre de priorité:
             a) Devoirs urgents (≤3 jours)
             b) Révisions de cours anciens (>7 jours)
             c) Apprentissage rotatif des 8 matières
        
        Args:
            week_start_date (date): Date du lundi de la semaine à planifier
        
        Returns:
            int: Nombre total d'activités planifiées
        """
        if isinstance(week_start_date, str):
            week_start_date = datetime.strptime(week_start_date, '%Y-%m-%d').date()
        
        # Supprimer l'ancien planning de cette semaine
        query = """
            DELETE FROM schedule_slots 
            WHERE date >= %s AND date < DATE_ADD(%s, INTERVAL 7 DAY)
        """
        DatabaseManager.execute_query(query, (week_start_date, week_start_date))
        
        # Récupérer les données
        courses = Course.get_courses_by_week(week_start_date)
        homework_list = list(Homework.get_urgent_homework())
        courses_to_revise = list(Course.get_courses_for_revision())
        subjects = LearningSubject.get_least_studied()
        
        schedule_entries = []
        subject_index = 0
        
        print(f"\n📅 Génération du planning pour la semaine du {week_start_date}")
        print(f"   📚 {len(courses)} cours")
        print(f"   ✏️  {len(homework_list)} devoirs urgents")
        print(f"   🔄 {len(courses_to_revise)} cours à réviser")
        print(f"   📖 {len(subjects)} matières d'apprentissage\n")
        
        # Planifier pour chaque jour de la semaine
        for day_offset in range(7):
            current_date = week_start_date + timedelta(days=day_offset)
            day_name = Scheduler.get_day_name(current_date)
            
            print(f"📌 {day_name} {current_date.strftime('%d/%m/%Y')}")
            
            # Ajouter les cours du jour
            daily_courses = 0
            for course in courses:
                course_date = course['week_date']
                if isinstance(course_date, str):
                    course_date = datetime.strptime(course_date, '%Y-%m-%d').date()
                
                if course_date == current_date:
                    schedule_entries.append((
                        current_date, 
                        course['start_time'], 
                        course['end_time'],
                        'course', 
                        course['name'], 
                        f"Cours: {course['name']}"
                    ))
                    daily_courses += 1
            
            if daily_courses > 0:
                print(f"   🎓 {daily_courses} cours planifiés")
            
            # Obtenir les créneaux libres
            free_slots = Scheduler.get_free_slots(current_date, courses)
            
            if not free_slots:
                print(f"   ⚠️  Aucun créneau libre\n")
                continue
            
            # Planifier dans les créneaux libres
            daily_activities = 0
            
            for slot_start, slot_end in free_slots:
                available_minutes = slot_end - slot_start
                
                # Si créneau trop court (moins de 1h), ignorer
                if available_minutes < 60:
                    continue
                
                current_time = slot_start
                
                # Remplir le créneau avec des sessions
                while current_time + PLANNING_CONFIG['session_duration'] <= slot_end:
                    session_start = Scheduler.minutes_to_time(current_time)
                    session_end = Scheduler.minutes_to_time(
                        current_time + PLANNING_CONFIG['session_duration']
                    )
                    
                    activity_added = False
                    
                    # PRIORITÉ 1: Devoirs urgents
                    for hw in homework_list[:]:  # Copie pour pouvoir modifier
                        due_date = hw['due_date']
                        if isinstance(due_date, str):
                            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                        
                        days_until_due = (due_date - current_date).days
                        
                        if 0 <= days_until_due <= PLANNING_CONFIG['homework_preparation_days']:
                            schedule_entries.append((
                                current_date, 
                                session_start, 
                                session_end,
                                'homework', 
                                hw['subject'], 
                                f"Préparation devoir: {hw['subject']}"
                            ))
                            homework_list.remove(hw)
                            activity_added = True
                            daily_activities += 1
                            break
                    
                    if activity_added:
                        current_time += PLANNING_CONFIG['session_duration'] + PLANNING_CONFIG['break_duration']
                        continue
                    
                    # PRIORITÉ 2: Révisions (en début de semaine)
                    if courses_to_revise and day_offset < 4:
                        course_to_revise = courses_to_revise.pop(0)
                        schedule_entries.append((
                            current_date, 
                            session_start, 
                            session_end,
                            'revision', 
                            course_to_revise['name'],
                            f"Révision: {course_to_revise['name']}"
                        ))
                        Course.mark_as_revised(course_to_revise['id'])
                        activity_added = True
                        daily_activities += 1
                        current_time += PLANNING_CONFIG['session_duration'] + PLANNING_CONFIG['break_duration']
                        continue
                    
                    # PRIORITÉ 3: Apprentissage rotatif
                    if subjects:
                        subject = subjects[subject_index % len(subjects)]
                        schedule_entries.append((
                            current_date, 
                            session_start, 
                            session_end,
                            'learning', 
                            subject['name'],
                            f"Apprentissage: {subject['name']}"
                        ))
                        
                        # Mettre à jour le temps d'étude
                        hours_studied = PLANNING_CONFIG['session_duration'] / 60
                        LearningSubject.update_study_time(subject['name'], hours_studied)
                        
                        subject_index += 1
                        daily_activities += 1
                    
                    current_time += PLANNING_CONFIG['session_duration'] + PLANNING_CONFIG['break_duration']
            
            if daily_activities > 0:
                print(f"   ✅ {daily_activities} activités d'apprentissage planifiées")
            print()
        
        # Insérer tous les créneaux dans la base de données
        if schedule_entries:
            query = """
                INSERT INTO schedule_slots 
                (date, start_time, end_time, activity_type, subject, description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            DatabaseManager.execute_many(query, schedule_entries)
        
        print(f"✅ Planning généré: {len(schedule_entries)} activités au total\n")
        
        return len(schedule_entries)
    
    @staticmethod
    def get_weekly_summary(week_start_date):
        """
        Génère un résumé du planning de la semaine.
        
        Args:
            week_start_date (date): Date du lundi
        
        Returns:
            dict: Résumé avec statistiques
        """
        query = """
            SELECT 
                activity_type,
                COUNT(*) as count,
                SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) as total_minutes
            FROM schedule_slots
            WHERE date >= %s AND date < DATE_ADD(%s, INTERVAL 7 DAY)
            GROUP BY activity_type
        """
        
        results = DatabaseManager.execute_query(
            query, (week_start_date, week_start_date), fetch=True
        )
        
        summary = {
            'course': {'count': 0, 'hours': 0},
            'homework': {'count': 0, 'hours': 0},
            'learning': {'count': 0, 'hours': 0},
            'revision': {'count': 0, 'hours': 0}
        }
        
        for row in results:
            activity = row['activity_type']
            summary[activity]['count'] = row['count']
            summary[activity]['hours'] = round(row['total_minutes'] / 60, 1)
        
        return summary