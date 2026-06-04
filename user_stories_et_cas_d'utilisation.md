# User Stories et Cas d’Utilisation (Use Cases)

# IFRI MentorLink v1

## 1\. Introduction

Ce document décrit les interactions possibles entre les utilisateurs et IFRI MentorLink.

Les User Stories permettent d’exprimer les besoins métier du point de vue de l’utilisateur.

Les Cas d’Utilisation décrivent les actions que le système doit permettre.

# 2\. Acteur principal

## Étudiant IFRI

L’étudiant est l’unique acteur principal du système.

Selon ses besoins, il peut agir comme :

- Mentor
- Mentoré
- Mentor et Mentoré simultanément

# 3\. Gestion des comptes

## US-001 : Créer un compte

En tant qu’étudiant,

Je souhaite créer un compte

Afin d’accéder à la plateforme.

### Critères d’acceptation

- Email obligatoire
- Téléphone obligatoire
- Email unique
- Téléphone unique
- Mot de passe obligatoire

## UC-001 : Inscription

Acteur :

- Étudiant

Scénario principal :

1.  L’utilisateur ouvre le formulaire d’inscription.
2.  Il renseigne ses informations.
3.  Le système vérifie l’unicité.
4.  Le système crée le compte.
5.  L’utilisateur est connecté.

Scénarios alternatifs :

- Email déjà utilisé.
- Téléphone déjà utilisé.
- Informations invalides.

## US-002 : Me connecter

En tant qu’utilisateur,

Je souhaite me connecter

Afin d’accéder à mon espace personnel.

## UC-002 : Connexion

Acteur :

- Utilisateur

Scénario principal :

1.  Saisie de l’identifiant.
2.  Saisie du mot de passe.
3.  Vérification.
4.  Connexion.

## US-003 : Réinitialiser mon mot de passe

En tant qu’utilisateur,

Je souhaite récupérer mon compte

Afin de retrouver l’accès à la plateforme.

# 4\. Gestion du profil

## US-004 : Compléter mon profil

En tant qu’utilisateur,

Je souhaite renseigner mes informations académiques

Afin d’améliorer les recommandations.

## UC-003 : Modifier son profil

Acteur :

- Utilisateur

Actions possibles :

- Modifier sa photo
- Modifier sa bio
- Modifier ses disponibilités
- Modifier ses compétences
- Modifier ses lacunes

# 5\. Gestion des compétences

## US-005 : Ajouter une compétence

En tant qu’utilisateur,

Je souhaite déclarer mes compétences

Afin d’aider d’autres étudiants.

## US-006 : Ajouter une lacune

En tant qu’utilisateur,

Je souhaite déclarer mes difficultés

Afin d’obtenir de l’aide.

## UC-004 : Gérer ses domaines

Acteur :

- Utilisateur

Actions possibles :

- Ajouter
- Modifier
- Supprimer

Compétences et lacunes.

# 6\. Gestion des disponibilités

## US-007 : Définir mes disponibilités

En tant qu’utilisateur,

Je souhaite renseigner mes créneaux libres

Afin d’être mis en relation avec des étudiants compatibles.

## UC-005 : Gérer ses disponibilités

Acteur :

- Utilisateur

Actions :

- Ajouter un créneau
- Modifier un créneau
- Supprimer un créneau

# 7\. Publication de mentorat

## US-008 : Publier une offre

En tant que mentor,

Je souhaite publier une offre

Afin de proposer mon aide.

## UC-006 : Créer une offre

Acteur :

- Utilisateur

Informations :

- Domaines
- Disponibilités
- Mode de mentorat
- Description

Résultat :

Offre créée.

## US-009 : Publier une demande

En tant que mentoré,

Je souhaite publier une demande

Afin de trouver un accompagnement.

## UC-007 : Créer une demande

Acteur :

- Utilisateur

Informations :

- Domaines
- Disponibilités
- Mode souhaité
- Description

Résultat :

Demande créée.

# 8\. Recherche

## US-010 : Rechercher des offres

En tant qu’utilisateur,

Je souhaite rechercher des offres

Afin de trouver un mentor.

## US-011 : Rechercher des demandes

En tant qu’utilisateur,

Je souhaite rechercher des demandes

Afin de trouver des mentorés.

## UC-008 : Rechercher une publication

Filtres possibles :

- Domaine
- Filière
- Niveau
- Disponibilités

# 9\. Réponses aux publications

## US-012 : Répondre à une offre

En tant qu’utilisateur,

Je souhaite répondre à une offre

Afin d’entrer en contact avec un mentor.

## US-013 : Répondre à une demande

En tant qu’utilisateur,

Je souhaite répondre à une demande

Afin de proposer mon aide.

## UC-009 : Répondre à une publication

Acteur :

- Utilisateur

Scénario :

1.  Consultation de la publication.
2.  Envoi d’une réponse.
3.  Réponse enregistrée.

# 10\. Matching intelligent

## US-014 : Trouver automatiquement des mentors

En tant que mentoré,

Je souhaite recevoir des recommandations

Afin de trouver rapidement les meilleurs mentors.

## US-015 : Trouver automatiquement des mentorés

En tant que mentor,

Je souhaite recevoir des recommandations

Afin d’aider les étudiants les plus compatibles.

## UC-010 : Calculer les compatibilités

Acteur :

- Système

Le système :

1.  Analyse les domaines.
2.  Analyse les disponibilités.
3.  Analyse les filières.
4.  Analyse les niveaux.
5.  Calcule un score.
6.  Classe les résultats.

# 11\. Gestion des réponses

## US-016 : Consulter les réponses reçues

En tant qu’utilisateur,

Je souhaite voir les personnes intéressées

Afin de choisir la meilleure correspondance.

## UC-011 : Accepter une réponse

Acteur :

- Créateur de la publication

Scénario :

1.  Consultation des réponses.
2.  Sélection d’une réponse.
3.  Acceptation.

Résultat :

Création d’une relation de mentorat.

## UC-012 : Refuser une réponse

Acteur :

- Créateur de la publication

Résultat :

Réponse marquée comme refusée.

# 12\. Relation mentor-mentoré

## US-017 : Gérer mes relations de mentorat

En tant qu’utilisateur,

Je souhaite suivre mes mentorats

Afin d’organiser mes activités.

## UC-013 : Consulter ses relations

L’utilisateur visualise :

- Relations actives
- Relations terminées
- Relations suspendues

## UC-014 : Clôturer une relation

Acteur :

- Mentor
- Mentoré

Résultat :

Relation marquée comme terminée.

# 13\. Messagerie

## US-018 : Envoyer un message

En tant qu’utilisateur,

Je souhaite communiquer avec mon mentor ou mentoré

Afin d’organiser les séances de mentorat.

## US-019 : Recevoir un message

En tant qu’utilisateur,

Je souhaite recevoir les messages en temps réel

Afin de communiquer efficacement.

## UC-015 : Envoyer un message

Scénario :

1.  Ouverture de la conversation.
2.  Rédaction du message.
3.  Envoi.
4.  Réception par le destinataire.

## UC-016 : Consulter l’historique

Acteur :

- Utilisateur

Résultat :

Accès à l’ensemble des messages échangés.

# 14\. Notifications

## US-020 : Être notifié

En tant qu’utilisateur,

Je souhaite recevoir des notifications

Afin d’être informé des nouveaux événements.

## UC-017 : Notification de nouveau message

Déclencheur :

Réception d’un message.

Résultat :

Notification affichée.

# 15\. Administration implicite

## US-021 : Maintenir la cohérence du système

En tant que système,

Je souhaite contrôler les données

Afin de garantir leur cohérence.

Exemples :

- Emails uniques
- Téléphones uniques
- Disponibilités valides
- Relations cohérentes

# 16\. MVP IFRI MentorLink v1

Les fonctionnalités obligatoires de la première version sont :

✅ Gestion des comptes

✅ Gestion des profils

✅ Gestion des compétences

✅ Gestion des lacunes

✅ Gestion des disponibilités

✅ Offres de mentorat

✅ Demandes de mentorat

✅ Réponses aux publications

✅ Matching intelligent

✅ Relations mentor-mentoré

✅ Messagerie textuelle

✅ Notifications temps réel

Les fonctionnalités suivantes sont reportées à une version future :

❌ Appels vidéo

❌ Partage de fichiers

❌ Réputation

❌ Évaluation des mentors

❌ Validation des compétences