-- Création de la base de données pour le planificateur d'apprentissage
-- Exécuter ce fichier avec: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS learning_planner 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE learning_planner;

-- ============================================
-- Table des cours
-- ============================================
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT 'Nom du cours',
    day_of_week VARCHAR(20) NOT NULL COMMENT 'Jour de la semaine',
    start_time TIME NOT NULL COMMENT 'Heure de début',
    end_time TIME NOT NULL COMMENT 'Heure de fin',
    week_date DATE NOT NULL COMMENT 'Date du début de la semaine',
    needs_revision BOOLEAN DEFAULT FALSE COMMENT 'Indique si une révision est nécessaire',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_week_date (week_date),
    INDEX idx_day (day_of_week)
) ENGINE=InnoDB COMMENT='Stocke les cours de chaque semaine';

-- ============================================
-- Table des devoirs
-- ============================================
CREATE TABLE IF NOT EXISTS homework (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(255) NOT NULL COMMENT 'Matière du devoir',
    description TEXT COMMENT 'Description détaillée',
    due_date DATE NOT NULL COMMENT 'Date limite',
    due_time TIME NOT NULL COMMENT 'Heure limite',
    preparation_days INT DEFAULT 3 COMMENT 'Nombre de jours pour préparer',
    status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_due_date (due_date),
    INDEX idx_status (status)
) ENGINE=InnoDB COMMENT='Gestion des devoirs à rendre';

-- ============================================
-- Table des matières d'apprentissage
-- ============================================
CREATE TABLE IF NOT EXISTS learning_subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE COMMENT 'Nom de la matière',
    priority INT DEFAULT 1 COMMENT 'Priorité (1-5)',
    last_studied DATETIME COMMENT 'Dernière fois étudiée',
    total_hours FLOAT DEFAULT 0 COMMENT 'Total heures étudiées',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_last_studied (last_studied),
    INDEX idx_priority (priority)
) ENGINE=InnoDB COMMENT='Matières à apprendre régulièrement';

-- ============================================
-- Table des créneaux planifiés
-- ============================================
CREATE TABLE IF NOT EXISTS schedule_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL COMMENT 'Date du créneau',
    start_time TIME NOT NULL COMMENT 'Heure de début',
    end_time TIME NOT NULL COMMENT 'Heure de fin',
    activity_type ENUM('course', 'homework', 'learning', 'revision') NOT NULL,
    subject VARCHAR(255) NOT NULL COMMENT 'Nom de la matière/cours',
    description TEXT COMMENT 'Description de l\'activité',
    notified BOOLEAN DEFAULT FALSE COMMENT 'Notification envoyée',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_date_time (date, start_time),
    INDEX idx_activity (activity_type),
    INDEX idx_notified (notified)
) ENGINE=InnoDB COMMENT='Planning détaillé par créneau horaire';

-- ============================================
-- Insertion des matières d'apprentissage par défaut
-- ============================================
INSERT INTO learning_subjects (name, priority) VALUES
    ('Python', 1),
    ('HTML', 1),
    ('CSS', 1),
    ('PHP', 1),
    ('MySQL', 1),
    ('PostgreSQL', 1),
    ('Math_General', 1),
    ('Lire_la_Bible', 1)
ON DUPLICATE KEY UPDATE name=name;

-- ============================================
-- Table d'historique (optionnel, pour statistiques)
-- ============================================
CREATE TABLE IF NOT EXISTS study_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    study_date DATE NOT NULL,
    duration_minutes INT NOT NULL,
    activity_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_date (study_date),
    INDEX idx_subject (subject_name)
) ENGINE=InnoDB COMMENT='Historique des sessions d\'étude';

-- Afficher les tables créées
SHOW TABLES;