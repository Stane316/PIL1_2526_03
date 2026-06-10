# IFRI MentorLink

## Projet Intégrateur — PIL1 2025-2026

IFRI MentorLink est une plateforme web de mentorat académique et professionnel développée dans le cadre du Projet Intégrateur de Licence 1 à l’IFRI.

L’application permet la mise en relation entre étudiants mentors et mentorés selon :

- leurs compétences,
- leurs lacunes,
- leurs disponibilités,
- leur filière,
- leur niveau académique.

# Équipe — Groupe 03

## Membres

- Stane ANIAMBOSSOU
- GUEDOU Deo-Gratias Tédy S.
- ANICLE Marco
- CHOUBADE Samadh
- NATTA YORI Alexandre
- OGOUGBE Babatundé Abdoulaye

# Équipe pédagogique

## Supervision

- M. Ratheil HOUNDJI

## Encadrants

- M. Armand ACCROMBESSI
- Mme Maryse GAHOU

# Technologies utilisées

## Backend

- Python
- Django

## Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript

## Base de données

- PostgreSQL

## Outils collaboratifs

- Git
- GitHub

# Fonctionnalités principales

## Authentification

- Inscription
- Connexion
- Réinitialisation du mot de passe
- Gestion des sessions

## Gestion des profils

- Informations personnelles
- Filière et niveau
- Compétences
- Lacunes
- Disponibilités
- Photo de profil

## Mentorat

- Création d’offres
- Création de demandes
- Consultation des offres
- Consultation des demandes

## Matching intelligent

Le système propose automatiquement des correspondances mentor/mentoré selon :

- compatibilité des matières (60%)
- compatibilité des disponibilités (20%)
- proximité des filières (10%)
- proximité des niveaux (10%)

## Messagerie

- Conversations privées
- Historique des messages
- Notifications

## Dashboard

- Tableau de bord utilisateur
- Navigation centralisée
- Gestion des activités

# Architecture du projet

backend/  
│  
├── accounts/  
├── publications/  
├── matching/  
├── mentorat/  
├── messaging/  
├── notifications/  
├── core/  
├── templates/  
├── static/  
├── media/  
└── manage.py

# Installation du projet

## 1\. Cloner le dépôt

git clone &lt;url-du-repository&gt;

## 2\. Entrer dans le projet

cd PIL1_2526_03

## 3\. Accéder au backend

cd backend

## 4\. Créer un environnement virtuel

### Windows

python -m venv .venv

## 5\. Activer l’environnement virtuel

### PowerShell

.venv\\Scripts\\Activate.ps1

## 6\. Installer les dépendances

pip install -r requirements.txt

## 7\. Configurer PostgreSQL

Créer une base nommée :

mentorlink_db

## 8\. Créer le fichier .env

Créer un fichier .env dans le dossier backend :

DEBUG=True  
<br/>SECRET_KEY=django-insecure-secret-key  
<br/>DB_NAME=mentorlink_db  
DB_USER=postgres  
DB_PASSWORD=your_password  
DB_HOST=localhost  
DB_PORT=5432

## 9\. Importer la base SQL

Importer :

mentorlink.sql

dans PostgreSQL via pgAdmin.

## 10\. Appliquer les migrations

python manage.py makemigrations  
python manage.py migrate

## 11\. Vérifier le projet

python manage.py check

## 12\. Lancer le serveur

python manage.py runserver

# Accès à l’application

http://127.0.0.1:8000/

# Structure Git

## Branches principales

- main
- develop
- feature/integration-frontend-backend

Branches secondaires :

- feature-auth
- feature-dashboard
- feature-mentorat
- feature-matching
- etc.

# Organisation du travail

Le projet a été développé selon une organisation collaborative :

- réunions quotidiennes,
- documentation continue,
- répartition modulaire des tâches,
- workflow GitHub,
- intégration progressive frontend/backend.

Chaque membre documentait régulièrement son avancement via des work logs individuels.

# Difficultés rencontrées

- Intégration frontend/backend Django
- Gestion des routes et templates
- Conflits Git
- Coordination de l’équipe
- Gestion du temps
- Adaptation des templates HTML à Django

# Solutions apportées

- Architecture modulaire
- Réunions quotidiennes
- Documentation obligatoire
- Découpage des responsabilités
- Workflow Git structuré
- Validation continue des fonctionnalités

# État final du projet

Le projet IFRI MentorLink est fonctionnel et répond globalement aux exigences du cahier des charges.

Certaines optimisations et phases de tests restent possibles pour améliorer davantage :

- les performances,
- l’expérience utilisateur,
- les validations frontend/backend,
- l’optimisation visuelle.

# Licence

Projet académique réalisé dans le cadre du Projet Intégrateur de Licence 1 — IFRI.

# Remerciements

Nous remercions :

- nos encadrants,
- l’équipe pédagogique,
- ainsi que tous les membres du groupe pour leur implication dans la réalisation du projet.