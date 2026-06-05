# MLD IFRI MentorLink v1

## Version 1.0 — Modèle Logique de Données PostgreSQL

# 1\. Objectif

Ce document transforme le MCD IFRI MentorLink v1 en un modèle logique directement exploitable dans PostgreSQL et Django ORM.

Principes retenus :

- PostgreSQL
- Normalisation 3NF
- Clés primaires auto-générées
- Clés étrangères explicites
- Contraintes d'intégrité
- Extensibilité future

# 2\. Table UTILISATEUR

utilisateur  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| nom | VARCHAR(100) |
| prenom | VARCHAR(100) |
| email | VARCHAR(255) UNIQUE |
| telephone | VARCHAR(30) UNIQUE |
| password_hash | VARCHAR(255) |
| photo_profil | TEXT NULL |
| bio | TEXT NULL |
| filiere | VARCHAR(50) |
| niveau | VARCHAR(20) |
| actif | BOOLEAN |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

# 3\. Table DOMAINE

domaine  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| nom | VARCHAR(150) UNIQUE |
| description | TEXT |
| valide | BOOLEAN |
| created_at | TIMESTAMP |

# 4\. Table DISPONIBILITE_UTILISATEUR

disponibilite_utilisateur  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| utilisateur_id | FK  |
| jour_semaine | SMALLINT |
| heure_debut | TIME |
| heure_fin | TIME |

# 5\. Table MAITRISE

Association Utilisateur ↔ Domaine

maitrise  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| utilisateur_id | FK  |
| domaine_id | FK  |
| niveau_maitrise | VARCHAR(20) |

Valeurs :

DEBUTANT  
INTERMEDIAIRE  
AVANCE  

Contrainte :

UNIQUE(utilisateur_id,domaine_id)  

# 6\. Table BESOIN

Association Utilisateur ↔ Domaine

besoin  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| utilisateur_id | FK  |
| domaine_id | FK  |
| niveau_priorite | SMALLINT |

Contrainte :

UNIQUE(utilisateur_id,domaine_id)  

# 7\. Table PUBLICATION

publication  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| auteur_id | FK utilisateur |
| type_publication | VARCHAR(20) |
| titre | VARCHAR(255) |
| description | TEXT |
| mode_mentorat | VARCHAR(20) |
| statut | VARCHAR(20) |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

# 8\. Table PUBLICATION_DOMAINE

Association Publication ↔ Domaine

publication_domaine  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| publication_id | FK  |
| domaine_id | FK  |
| statut_couverture | VARCHAR(20) |

Valeurs :

OUVERT  
COUVERT  
ABANDONNE  

Contrainte :

UNIQUE(publication_id,domaine_id)  

# 9\. Table DISPONIBILITE_PUBLICATION

disponibilite_publication  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| publication_id | FK  |
| jour_semaine | SMALLINT |
| heure_debut | TIME |
| heure_fin | TIME |

# 10\. Table REPONSE

reponse  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| publication_id | FK  |
| auteur_id | FK utilisateur |
| message | TEXT |
| statut | VARCHAR(20) |
| created_at | TIMESTAMP |

Valeurs :

EN_ATTENTE  
ACCEPTEE  
REFUSEE  

# 11\. Table REPONSE_DOMAINE

Association Réponse ↔ Domaine

reponse_domaine  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| reponse_id | FK  |
| domaine_id | FK  |

Contrainte :

UNIQUE(reponse_id,domaine_id)  

# 12\. Table RELATION_MENTORAT

⚠️ Ici nous devons faire une légère amélioration par rapport au MCD.

Une relation doit connaître :

- le mentor
- le mentoré

Donc :

relation_mentorat  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| mentor_id | FK utilisateur |
| mentore_id | FK utilisateur |
| reponse_id | FK  |
| statut | VARCHAR(20) |
| date_debut | TIMESTAMP |
| date_fin | TIMESTAMP NULL |
| commentaire_fin | TEXT NULL |

Valeurs :

ACTIVE  
SUSPENDUE  
TERMINEE  

# 13\. Table RELATION_DOMAINE

Après analyse approfondie, je recommande son ajout.

Pourquoi ?

Une même réponse peut couvrir :

Python  
SQL  
Linux  

Mais la progression doit être suivie domaine par domaine.

relation_domaine  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| relation_id | FK  |
| domaine_id | FK  |
| statut | VARCHAR(20) |

Valeurs :

EN_COURS  
MAITRISE  
ABANDONNE  

Contrainte :

UNIQUE(relation_id,domaine_id)  

# 14\. Table CONVERSATION

conversation  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| relation_id | FK UNIQUE |
| created_at | TIMESTAMP |

Une conversation par relation.

# 15\. Table MESSAGE

message  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| conversation_id | FK  |
| expediteur_id | FK utilisateur |
| contenu | TEXT |
| lu  | BOOLEAN |
| created_at | TIMESTAMP |

# 16\. Table NOTIFICATION

notification  

|     |     |
| --- | --- |
| **Champ** | **Type** |
| id  | BIGSERIAL PK |
| utilisateur_id | FK  |
| type_notification | VARCHAR(50) |
| contenu | TEXT |
| lu  | BOOLEAN |
| created_at | TIMESTAMP |

# 17\. Contraintes CHECK recommandées

## Filière

GL  
IA  
SIO  
CYBER  

ou les valeurs officielles de l'IFRI.

## Niveau

LICENCE_1  
LICENCE_2  
LICENCE_3  

## Type publication

OFFRE  
DEMANDE  

## Mode mentorat

PRESENTIEL  
EN_LIGNE  
HYBRIDE  

# 18\. Index à créer

CREATE INDEX idx_publication_type;  
CREATE INDEX idx_publication_statut;  
<br/>CREATE INDEX idx_reponse_publication;  
<br/>CREATE INDEX idx_message_conversation;  
<br/>CREATE INDEX idx_notification_utilisateur;  
<br/>CREATE INDEX idx_relation_mentor;  
<br/>CREATE INDEX idx_relation_mentore;  
<br/>CREATE INDEX idx_domaine_nom;  

# 19\. Structure finale de la base

UTILISATEUR  
│  
├── DISPONIBILITE_UTILISATEUR  
├── MAITRISE  
├── BESOIN  
├── PUBLICATION  
├── REPONSE  
├── MESSAGE  
└── NOTIFICATION  
<br/>DOMAINE  
│  
├── MAITRISE  
├── BESOIN  
├── PUBLICATION_DOMAINE  
├── REPONSE_DOMAINE  
└── RELATION_DOMAINE  
<br/>PUBLICATION  
│  
├── PUBLICATION_DOMAINE  
├── DISPONIBILITE_PUBLICATION  
└── REPONSE  
<br/>REPONSE  
│  
├── REPONSE_DOMAINE  
└── RELATION_MENTORAT  
<br/>RELATION_MENTORAT  
│  
├── RELATION_DOMAINE  
└── CONVERSATION  
<br/>CONVERSATION  
│  
└── MESSAGE  

# Validation Architecture

À ce stade, le projet est prêt pour :

Vision Fonctionnelle  
✅  
Glossaire Métier  
✅  
User Stories  
✅  
MCD  
✅  
MLD  
✅  

La prochaine étape sera normalement :

MPD IFRI MentorLink v1  
(Schéma PostgreSQL complet)  

où nous générerons les vraies instructions SQL (CREATE TABLE, contraintes, index, clés étrangères) puis le mapping Django ORM.