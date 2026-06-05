# team_first_sprint_ifri_mentorlink_v1.md

# IFRI MentorLink

## Sprint 0 : Mise en place des fondations

Version : 1.0

Objectif :

Construire les bases techniques, organisationnelles et collaboratives du projet afin que le développement effectif puisse commencer dans de bonnes conditions.

# Philosophie du Sprint 0

Aucun membre ne travaille seul.

Même si chaque membre possède une responsabilité principale, chacun doit comprendre le travail des autres.

Le Sprint 0 ne vise pas à terminer une fonctionnalité métier.

Il vise à préparer l’équipe.

# STAN

## Mission principale

Mettre en place l’organisation générale.

## Tâches techniques

### 1\. Finaliser la documentation existante

Vérifier que les documents suivants sont présents :

- Vision Fonctionnelle
- Glossaire et Règles Métier
- User Stories
- MCD
- MLD
- MPD
- Architecture Django
- GitHub Workflow
- Development Roadmap
- Team Organization
- Team Responsibilities
- Meeting Rules
- Team Directory

### 2\. Créer le dépôt GitHub

Actions :

- créer le dépôt ;
- configurer la branche principale ;
- ajouter le README ;
- ajouter le .gitignore ;
- ajouter les encadreurs ;
- ajouter les membres.

### 3\. Créer la structure du projet

Créer les dossiers :

backend/

frontend/

database/

docs/

meetings/

resources/

### 4\. Superviser les premiers commits

Objectif :

Chaque membre doit effectuer son premier commit.

## Livrable attendu

Le Sprint 0 est validé pour Stan lorsque :

- le dépôt GitHub est opérationnel ;
- tous les membres sont ajoutés ;
- tous les documents sont disponibles ;
- tous les membres ont effectué leur premier commit.

# ALEXANDRE

## Mission principale

Préparer le backend.

## Tâches techniques

### 1\. Installer Django

Créer un environnement virtuel.

Installer :

- Django
- psycopg2
- python-dotenv

### 2\. Créer le projet Django

Créer :

ifri_mentorlink/

Créer l’application :

users

### 3\. Configurer PostgreSQL

Préparer la connexion.

Tester :

python manage.py migrate

### 4\. Comprendre les modèles de données

Lire :

- MCD
- MLD
- MPD

Comprendre les relations.

## Livrable attendu

Le backend démarre.

La connexion PostgreSQL fonctionne.

Les migrations de base fonctionnent.

# MARCO

## Mission principale

Préparer le frontend.

## Tâches techniques

### 1\. Installer Bootstrap

Préparer la structure CSS.

### 2\. Construire le template principal

Créer :

- navbar
- footer
- structure générale

### 3\. Préparer les pages vides

Créer les templates :

- accueil
- connexion
- inscription
- profil
- dashboard

Le contenu peut être vide.

### 4\. Étudier les User Stories

Identifier les futurs composants visuels.

## Livrable attendu

Navigation fonctionnelle.

Pages accessibles.

Structure Bootstrap prête.

# ABDOULAYE

## Mission principale

Validation technique.

## Tâches techniques

### 1\. Relire le MPD

Vérifier :

- clés primaires ;
- clés étrangères ;
- cardinalités ;
- cohérence.

### 2\. Tester le script PostgreSQL

Exécuter la création de la base.

Vérifier qu’aucune erreur SQL n’apparaît.

### 3\. Préparer la stratégie de tests

Créer une liste :

- inscription ;
- connexion ;
- création publication ;
- matching ;
- messagerie.

### 4\. Relire la documentation

Identifier les zones ambiguës.

## Livrable attendu

Script SQL validé.

Liste initiale des tests produite.

Remarques techniques remontées.

# SAMADH

## Mission principale

Support Frontend.

## Tâches techniques

### 1\. Lire les User Stories.

Comprendre le parcours utilisateur.

### 2\. Créer les formulaires HTML

Préparer :

- inscription
- connexion

Simple HTML + Bootstrap.

Pas de logique backend.

### 3\. Étudier les templates Django

Comprendre :

- extends
- blocks
- include

### 4\. Faire une première revue UX

Noter les difficultés potentielles.

## Livrable attendu

Premiers formulaires prêts.

Compréhension du système de templates.

# TEDDY

## Mission principale

Documentation et soutien UX.

## Tâches techniques

### 1\. Relire toute la documentation.

Vérifier :

- orthographe ;
- cohérence ;
- compréhension.

### 2\. Préparer le modèle des comptes-rendus.

Créer le format standard.

### 3\. Préparer le squelette de la soutenance.

Créer un plan PowerPoint :

- contexte ;
- problème ;
- solution ;
- architecture ;
- démonstration ;
- perspectives.

### 4\. Observer l’expérience utilisateur.

Identifier les parties qui pourraient sembler compliquées.

## Livrable attendu

Modèle de compte-rendu prêt.

Plan de soutenance prêt.

Documentation relue.

# Objectif collectif du Sprint 0

À la fin du Sprint 0, l’équipe doit pouvoir dire :

✓ Nous avons compris le projet.

✓ Nous avons tous accès au dépôt GitHub.

✓ Nous savons utiliser Git.

✓ Le backend démarre.

✓ PostgreSQL fonctionne.

✓ Le frontend possède une structure.

✓ La documentation est commune.

✓ Chaque membre sait exactement ce qu’il doit faire pour le Sprint 1.

# Définition du Sprint 0 terminé

Le Sprint 0 est officiellement terminé lorsque les six responsables valident leurs livrables respectifs lors du meeting quotidien.