# github_workflow_ifri_mentorlink_v1

## Version 1.0 — Workflow Officiel du Projet IFRI MentorLink

# 1\. Objectif

Ce document définit :

- l'organisation GitHub ;
- les branches ;
- les règles de commit ;
- les Pull Requests ;
- la revue de code ;
- l'intégration continue de l'équipe.

# 2\. Création du dépôt

Nom recommandé :

ifri-mentorlink  

ou

IFRI-MentorLink  

Description :

Plateforme de mentorat académique et professionnel pour les étudiants de l'IFRI.  
Projet intégrateur 2026.  

# 3\. Membres du dépôt

Ajouter :

Tous les membres du groupe  

et obligatoirement :

ratheilesse  
primearwyn  
MaryseGAHOU  

comme demandé dans le cahier des charges.

# 4\. Structure du dépôt

ifri-mentorlink/  
<br/>├── backend/  
├── frontend/  
├── docs/  
├── scripts/  
├── .github/  
<br/>├── README.md  
├── .gitignore  
└── LICENSE  

# 5\. Stratégie de branches

## Branche principale

main  

Interdiction de développer dessus.

## Branche d'intégration

develop  

Toutes les fonctionnalités terminées arrivent ici.

## Branches de fonctionnalités

Format :

feature/&lt;nom&gt;  

Exemples :

feature/authentication  
<br/>feature/profile-management  
<br/>feature/publications  
<br/>feature/matching  
<br/>feature/messaging  
<br/>feature/notifications  
<br/>feature/frontend-auth  

# 6\. Workflow officiel

main  
↑  
<br/>develop  
↑  
<br/>feature/\*  

Cycle :

Créer feature  
<br/>Développer  
<br/>Commit  
<br/>Push  
<br/>Pull Request  
<br/>Review  
<br/>Merge vers develop  
<br/>Tests  
<br/>Release vers main  

# 7\. Interdictions

Aucun membre ne doit :

push directement sur main  

Aucun membre ne doit :

push directement sur develop  

Tout passe par :

Pull Request  

# 8\. Convention de commits

Format :

type(scope): description  

## Types autorisés

### Feature

feat:  

Exemple :

feat(auth): add user registration  

### Correction

fix:  

Exemple :

fix(profile): resolve avatar upload issue  

### Documentation

docs:  

Exemple :

docs(mcd): update mentoring relationship rules  

### Refactoring

refactor:  

Exemple :

refactor(matching): simplify compatibility calculation  

### Tests

test:  

Exemple :

test(auth): add registration tests  

# 9\. Taille des commits

Bon :

feat(auth): add login endpoint  
<br/>feat(auth): add JWT generation  
<br/>fix(auth): validate email uniqueness  

Mauvais :

final version  
<br/>all work done  
<br/>update project  

# 10\. Pull Requests

Titre :

\[FEATURE\] Authentication Module  

ou

\[FIX\] Messaging Bug  

Description minimale :

Résumé  
<br/>Fonctionnalités ajoutées  
<br/>Tests effectués  
<br/>Points à vérifier  

# 11\. Code Review

Avant chaque fusion :

Vérifier :

Le code fonctionne  
<br/>Pas d'erreurs  
<br/>Respect du style  
<br/>Respect de l'architecture  
<br/>Respect du cahier des charges  

# 12\. Checklist Pull Request

Chaque PR doit répondre :

☑ Fonctionnalité terminée  
<br/>☑ Tests effectués  
<br/>☑ Aucun bug connu  
<br/>☑ Documentation mise à jour  
<br/>☑ Respect de l'architecture  

# 13\. Documentation obligatoire

Chaque fonctionnalité importante doit mettre à jour :

docs/  

Exemples :

docs/authentication.md  
<br/>docs/matching.md  
<br/>docs/messaging.md  
<br/>docs/api.md  

# 14\. Répartition GitHub recommandée

## Responsable Architecture

Toi (Stan)

Responsabilités :

Validation architecture  
<br/>Validation MCD  
<br/>Validation MLD  
<br/>Validation MPD  
<br/>Validation PR critiques  

## Responsable Backend

Mentoring  
Matching  
Services  

## Responsable Messagerie

Messaging  
Notifications  

## Responsable Frontend

Pages  
Bootstrap  
UX  

## Responsable Documentation

README  
<br/>API  
<br/>Architecture  
<br/>Guides  

# 15\. README minimal

Le dépôt doit contenir :

Présentation du projet  
<br/>Objectifs  
<br/>Technologies  
<br/>Installation  
<br/>Lancement  
<br/>Contributeurs  

# 16\. Protection des branches

Configurer GitHub :

Pour main :

Require Pull Request  
<br/>Require Review  
<br/>Block Direct Push  

Pour develop :

Require Pull Request  

# 17\. Historique Git attendu

Les professeurs doivent voir :

feat(auth): registration endpoint  
<br/>feat(auth): JWT authentication  
<br/>feat(profile): profile update  
<br/>feat(publication): create mentoring request  
<br/>feat(matching): compatibility engine  
<br/>feat(chat): realtime messaging  
<br/>docs(api): add authentication endpoints  

et non :

update  
<br/>test  
<br/>final  
<br/>version finale  

# 18\. Critère de validation du workflow

Le workflow est considéré comme respecté lorsque :

☑ Tous les membres ont des commits  
<br/>☑ Les branches sont organisées  
<br/>☑ Les PR sont utilisées  
<br/>☑ Les professeurs ont accès au dépôt  
<br/>☑ La documentation est à jour  
<br/>☑ Le dépôt reflète clairement l'évolution du projet