# architecture_django_ifri_mentorlink_v1

## Version 1.0 — Architecture Applicative Officielle

# 1\. Objectif

Ce document définit l'architecture technique du backend IFRI MentorLink.

Son rôle est de :

- organiser le projet Django ;
- répartir le travail entre les membres ;
- faciliter la maintenance ;
- faciliter les tests ;
- préparer l'évolution future du projet.

# 2\. Principes d'Architecture

Nous allons utiliser :

### Backend

Python 3.13+  
Django 5+  
Django REST Framework  
PostgreSQL  

### Frontend

HTML  
CSS  
Javascript  
Bootstrap 5  

Pourquoi Bootstrap ?

- appris en cours ;
- rapide à développer ;
- faible courbe d'apprentissage ;
- idéal pour un projet de 10 jours.

### Architecture

Client  
↓  
REST API  
↓  
Django  
↓  
PostgreSQL  

Architecture :

Client-Serveur  

conforme au cahier des charges.

# 3\. Structure Générale du Projet

mentorlink/  
<br/>├── backend/  
│  
├── docs/  
│  
├── frontend/  
│  
├── scripts/  
│  
└── .github/  

# 4\. Structure Django

backend/  
<br/>├── manage.py  
│  
├── config/  
│  
├── apps/  
│  
│ ├── users/  
│ ├── domains/  
│ ├── mentoring/  
│ ├── messaging/  
│ └── notifications/  
│  
├── services/  
│  
├── common/  
│  
└── tests/  

# 5\. Application Users

## Responsabilité

Gestion des utilisateurs.

### Contient

Utilisateur  
DisponibiliteUtilisateur  
Maitrise  
Besoin  

### Models

User  
UserAvailability  
Mastery  
Need  

### API

POST /api/auth/register  
<br/>POST /api/auth/login  
<br/>POST /api/auth/forgot-password  
<br/>GET /api/users/profile  
<br/>PUT /api/users/profile  

### Responsable idéal

1 étudiant

# 6\. Application Domains

## Responsabilité

Gestion des domaines.

### Models

Domain  

### API

GET /api/domains  
<br/>POST /api/domains/suggest  

### Responsable

Peut être fusionnée avec Users.

# 7\. Application Mentoring

## Cœur du projet

Cette application contient :

Publication  
PublicationDomain  
<br/>Response  
ResponseDomain  
<br/>MentorshipRelation  
RelationDomain  
<br/>PublicationAvailability  

### Fonctionnalités

Création d'offres

Création de demandes

Matching

Acceptation

Refus

Suivi des mentorats

### API

POST /api/publications  
<br/>GET /api/publications  
<br/>GET /api/publications/{id}  
<br/>POST /api/publications/{id}/respond  
<br/>POST /api/responses/{id}/accept  
<br/>POST /api/responses/{id}/reject  

### Responsable

Étudiant Backend principal.

# 8\. Application Messaging

## Responsabilité

Messagerie temps réel.

### Models

Conversation  
<br/>Message  

### Technologies

Django Channels  
WebSockets  

### API

GET /api/conversations  
<br/>GET /api/conversations/{id}  
<br/>GET /api/messages  

### WebSocket

ws/chat/{conversation_id}  

### Responsable

1 étudiant.

# 9\. Application Notifications

## Responsabilité

Notifications système.

### Models

Notification  

### Exemples

Nouvelle réponse  
<br/>Réponse acceptée  
<br/>Nouveau message  
<br/>Mentorat terminé  

### API

GET /api/notifications  
<br/>PATCH /api/notifications/{id}/read  

# 10\. Dossier Services

Le dossier le plus important.

## Pourquoi ?

Les règles métier ne doivent pas être dans les vues.

### Mauvais

views.py  
800 lignes  

### Bon

services/  

# Structure

services/  
<br/>├── matching_service.py  
├── mentorship_service.py  
├── notification_service.py  
├── availability_service.py  
└── statistics_service.py  

# 11\. Matching Service

## Mission

Calculer le score de compatibilité.

### Entrées

Publication  
<br/>Utilisateur  

### Sortie

Score de compatibilité  

### Critères

#### Domaines

Poids :

50 %  

#### Disponibilités

Poids :

30 %  

#### Filière

Poids :

10 %  

#### Niveau

Poids :

10 %  

### Formule

ScoreFinal  
<br/>\=  
Domaines  
+  
Disponibilités  
+  
Filière  
+  
Niveau  

sur 100.

# 12\. Dossier Common

Code partagé.

common/  
<br/>├── constants.py  
├── permissions.py  
├── validators.py  
├── exceptions.py  
└── pagination.py  

# 13\. Authentification

Utiliser :

Django Authentication  

JWT  

via :

SimpleJWT  

# 14\. Permissions

## Utilisateur connecté

IsAuthenticated  

## Auteur publication

CanEditPublication  

## Participant conversation

CanAccessConversation  

# 15\. Tests

Chaque application possède :

tests/  
<br/>test_users.py  
<br/>test_publications.py  
<br/>test_matching.py  
<br/>test_messaging.py  

# 16\. Architecture Frontend

frontend/  
<br/>├── pages/  
│  
├── css/  
│  
├── js/  
│  
└── assets/  

# Pages MVP

## Auth

login.html  
<br/>register.html  
<br/>forgot_password.html  

## Profil

profile.html  

## Mentorat

publications.html  
<br/>publication_details.html  
<br/>create_publication.html  
<br/>matching_results.html  

## Messagerie

chat.html  

## Notifications

notifications.html  

# 17\. Répartition idéale équipe (6 personnes)

### Développeur 1

Users  
Auth  
Profil  

### Développeur 2

Domains  
Compétences  
Lacunes  

### Développeur 3

Mentoring  
Publications  

### Développeur 4

Matching  
Services  

### Développeur 5

Messaging  
WebSocket  

### Développeur 6

Frontend  
Bootstrap  
Intégration UI  

# 18\. Roadmap Technique

Phase 1

Architecture  
✅  

Phase 2

GitHub  
Création dépôt  
Branches  
Workflow  

Phase 3

Création projet Django  

Phase 4

Base PostgreSQL  
Migration  

Phase 5

Développement backend  

Phase 6

Développement frontend  

Phase 7

Tests  

Phase 8

Soutenance