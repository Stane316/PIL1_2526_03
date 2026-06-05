# MCD IFRI MentorLink v1

## Version Finale Validée

### Projet Intégrateur IFRI

# 1\. Présentation

Le présent document définit le Modèle Conceptuel de Données (MCD) de l’application IFRI MentorLink.

L’objectif de l’application est de mettre en relation des étudiants de l’IFRI dans le cadre du mentorat académique et professionnel.

Le modèle a été conçu pour :

- respecter le cahier des charges ;
- faciliter le matching mentor/mentoré ;
- permettre l’évolution future du système ;
- assurer la cohérence des données ;
- faciliter l’implémentation avec PostgreSQL et Django.

# 2\. Entités Principales

## UTILISATEUR

Représente un étudiant inscrit sur la plateforme.

### Attributs

- id_utilisateur (PK)
- nom
- prenom
- email
- telephone
- mot_de_passe_hash
- photo_profil
- bio
- filiere
- niveau
- actif
- date_creation
- date_modification

### Contraintes

- email unique
- telephone unique

## DOMAINE

Représente une matière ou compétence académique.

### Exemples

- Python
- SQL
- Java
- Linux
- Cybersécurité
- Intelligence Artificielle
- Git
- Docker

### Attributs

- id_domaine (PK)
- nom
- description
- valide
- date_creation

### Contraintes

- nom unique

### Règles métier

La liste des domaines est prédéfinie.

Un étudiant peut proposer un nouveau domaine.

Le domaine proposé devra être validé avant utilisation.

## DISPONIBILITE_UTILISATEUR

Créneaux habituels d’un utilisateur.

### Attributs

- id_disponibilite_utilisateur (PK)
- jour_semaine
- heure_debut
- heure_fin

## PUBLICATION

Offre ou demande de mentorat.

### Attributs

- id_publication (PK)
- type_publication
- titre
- description
- mode_mentorat
- statut
- date_creation
- date_modification

### TypePublication

- OFFRE
- DEMANDE

### ModeMentorat

- PRESENTIEL
- EN_LIGNE
- HYBRIDE

### StatutPublication

- OUVERTE
- FERMEE
- ARCHIVEE

## DISPONIBILITE_PUBLICATION

Disponibilités spécifiques à une publication.

### Attributs

- id_disponibilite_publication (PK)
- jour_semaine
- heure_debut
- heure_fin

## REPONSE

Réponse apportée à une publication.

### Attributs

- id_reponse (PK)
- message
- statut
- date_creation

### StatutRéponse

- EN_ATTENTE
- ACCEPTEE
- REFUSEE

## RELATION_MENTORAT

Relation créée après acceptation d’une réponse.

### Attributs

- id_relation (PK)
- statut
- date_debut
- date_fin
- commentaire_fin

### StatutRelation

- ACTIVE
- TERMINEE
- SUSPENDUE

## CONVERSATION

Conversation associée à une relation de mentorat.

### Attributs

- id_conversation (PK)
- date_creation

## MESSAGE

Message envoyé dans une conversation.

### Attributs

- id_message (PK)
- contenu
- lu
- date_envoi

## NOTIFICATION

Notification reçue par un utilisateur.

### Attributs

- id_notification (PK)
- type_notification
- contenu
- lu
- date_creation

# 3\. Associations Métier

## MAITRISE

Permet de déclarer les compétences maîtrisées par un utilisateur.

### Attributs

- niveau_maitrise

### Valeurs

- DEBUTANT
- INTERMEDIAIRE
- AVANCE

### Règle métier

Un utilisateur ne peut être mentor que pour un domaine dont le niveau est :

- INTERMEDIAIRE
- AVANCE

### Cardinalités

UTILISATEUR (0,N) ←→ DOMAINE (0,N)

## BESOIN

Permet de déclarer les lacunes d’un utilisateur.

### Attributs

- niveau_priorite

### Cardinalités

UTILISATEUR (0,N) ←→ DOMAINE (0,N)

## PUBLICATION_DOMAINE

Associe une publication aux domaines concernés.

### Attributs

- statut_couverture

### Valeurs

- OUVERT
- COUVERT
- ABANDONNE

### Cardinalités

PUBLICATION (1,N) ←→ DOMAINE (1,N)

### Règle métier

Une publication peut concerner plusieurs domaines.

Exemple :

Publication :

- Python
- SQL
- Linux

Chaque domaine possède son propre statut de couverture.

## REPONSE_DOMAINE

Permet à un répondant d’indiquer les domaines qu’il couvre réellement.

### Cardinalités

REPONSE (1,N) ←→ DOMAINE (1,N)

### Exemple

Publication :

- Python
- SQL
- Linux

Réponse :

- Python
- Linux

Le répondant couvre uniquement ces domaines.

# 4\. Relations Entre Entités

## UTILISATEUR → DISPONIBILITE_UTILISATEUR

Un utilisateur possède plusieurs disponibilités.

Cardinalité :

UTILISATEUR (1,1) → DISPONIBILITE_UTILISATEUR (0,N)

## UTILISATEUR → PUBLICATION

Un utilisateur peut créer plusieurs publications.

Cardinalité :

UTILISATEUR (1,1) → PUBLICATION (0,N)

## PUBLICATION → DISPONIBILITE_PUBLICATION

Une publication peut posséder plusieurs créneaux.

Cardinalité :

PUBLICATION (1,1) → DISPONIBILITE_PUBLICATION (0,N)

## PUBLICATION → REPONSE

Une publication peut recevoir plusieurs réponses.

Cardinalité :

PUBLICATION (1,1) → REPONSE (0,N)

## UTILISATEUR → REPONSE

Un utilisateur peut répondre à plusieurs publications.

Cardinalité :

UTILISATEUR (1,1) → REPONSE (0,N)

## REPONSE → RELATION_MENTORAT

Une réponse acceptée crée une relation de mentorat.

Cardinalité :

REPONSE (0,1) → RELATION_MENTORAT (1,1)

## RELATION_MENTORAT → CONVERSATION

Chaque relation possède une conversation unique.

Cardinalité :

RELATION_MENTORAT (1,1) → CONVERSATION (1,1)

## CONVERSATION → MESSAGE

Une conversation contient plusieurs messages.

Cardinalité :

CONVERSATION (1,1) → MESSAGE (0,N)

## UTILISATEUR → MESSAGE

Un utilisateur peut envoyer plusieurs messages.

Cardinalité :

UTILISATEUR (1,1) → MESSAGE (0,N)

## UTILISATEUR → NOTIFICATION

Un utilisateur reçoit plusieurs notifications.

Cardinalité :

UTILISATEUR (1,1) → NOTIFICATION (0,N)

# 5\. Règles Métier Fondamentales

## RM-01

Un email est unique.

## RM-02

Un numéro de téléphone est unique.

## RM-03

Les mots de passe sont stockés sous forme hashée.

## RM-04

Un utilisateur peut être mentor et mentoré simultanément.

## RM-05

Une publication peut concerner plusieurs domaines.

## RM-06

Une réponse peut couvrir seulement une partie des domaines d’une publication.

## RM-07

Une publication reste ouverte tant qu’au moins un domaine possède le statut OUVERT.

## RM-08

Une publication est automatiquement fermée lorsque tous ses domaines sont couverts ou abandonnés.

## RM-09

Un mentor peut accompagner plusieurs mentorés.

## RM-10

Un mentoré peut avoir plusieurs mentors.

## RM-11

Une relation de mentorat est créée uniquement après acceptation d’une réponse.

## RM-12

Une conversation est créée automatiquement lors de la création d’une relation de mentorat.

## RM-13

L’historique des messages est conservé.

## RM-14

Les notifications peuvent être conservées pour consultation ultérieure.

# 6\. Validation

Ce document constitue la référence métier officielle du projet IFRI MentorLink v1.

Toute implémentation PostgreSQL, Django, API REST ou Frontend devra respecter ce modèle.