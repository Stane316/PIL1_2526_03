# MPD IFRI MentorLink v1

## Version 1.0 — Schéma Physique PostgreSQL

Ce document constitue la version physique de la base de données IFRI MentorLink destinée à PostgreSQL. Il s'appuie sur les bonnes pratiques PostgreSQL concernant les clés primaires, contraintes d'intégrité et clés étrangères. ([PostgreSQL](https://www.postgresql.org/docs/current/sql-createtable.html?utm_source=chatgpt.com))

# 1\. Création des types ENUM

CREATE TYPE filiere_enum AS ENUM (  
'GL',  
'IA',  
'SEIOT',  
'CYBERSECURITE',

'IM'  
);  
<br/>CREATE TYPE niveau_enum AS ENUM (  
'LICENCE_1',  
'LICENCE_2',  
'LICENCE_3'  
);  
<br/>CREATE TYPE niveau_maitrise_enum AS ENUM (  
'DEBUTANT',  
'INTERMEDIAIRE',  
'AVANCE'  
);  
<br/>CREATE TYPE type_publication_enum AS ENUM (  
'OFFRE',  
'DEMANDE'  
);  
<br/>CREATE TYPE mode_mentorat_enum AS ENUM (  
'PRESENTIEL',  
'EN_LIGNE',  
'HYBRIDE'  
);  
<br/>CREATE TYPE statut_publication_enum AS ENUM (  
'OUVERTE',  
'FERMEE',  
'ARCHIVEE'  
);  
<br/>CREATE TYPE statut_reponse_enum AS ENUM (  
'EN_ATTENTE',  
'ACCEPTEE',  
'REFUSEE'  
);  
<br/>CREATE TYPE statut_relation_enum AS ENUM (  
'ACTIVE',  
'SUSPENDUE',  
'TERMINEE'  
);  
<br/>CREATE TYPE statut_couverture_enum AS ENUM (  
'OUVERT',  
'COUVERT',  
'ABANDONNE'  
);  
<br/>CREATE TYPE statut_relation_domaine_enum AS ENUM (  
'EN_COURS',  
'MAITRISE',  
'ABANDONNE'  
);  

# 2\. Table utilisateur

CREATE TABLE utilisateur (  
id BIGSERIAL PRIMARY KEY,  
<br/>nom VARCHAR(100) NOT NULL,  
prenom VARCHAR(100) NOT NULL,  
<br/>email VARCHAR(255) NOT NULL UNIQUE,  
telephone VARCHAR(30) NOT NULL UNIQUE,  
<br/>password_hash VARCHAR(255) NOT NULL,  
<br/>photo_profil TEXT,  
<br/>bio TEXT,  
<br/>filiere filiere_enum NOT NULL,  
niveau niveau_enum NOT NULL,  
<br/>actif BOOLEAN NOT NULL DEFAULT TRUE,  
<br/>created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  
);  

# 3\. Table domaine

CREATE TABLE domaine (  
id BIGSERIAL PRIMARY KEY,  
<br/>nom VARCHAR(150) NOT NULL UNIQUE,  
<br/>description TEXT,  
<br/>valide BOOLEAN NOT NULL DEFAULT TRUE,  
<br/>created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  
);  

# 4\. Disponibilités utilisateur

CREATE TABLE disponibilite_utilisateur (  
id BIGSERIAL PRIMARY KEY,  
<br/>utilisateur_id BIGINT NOT NULL,  
<br/>jour_semaine SMALLINT NOT NULL  
CHECK (jour_semaine BETWEEN 1 AND 7),  
<br/>heure_debut TIME NOT NULL,  
heure_fin TIME NOT NULL,  
<br/>CONSTRAINT fk_dispo_user  
FOREIGN KEY (utilisateur_id)  
REFERENCES utilisateur(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT chk_dispo_user_heure  
CHECK (heure_fin > heure_debut)  
);  

# 5\. Maîtrises

CREATE TABLE maitrise (  
id BIGSERIAL PRIMARY KEY,  
<br/>utilisateur_id BIGINT NOT NULL,  
domaine_id BIGINT NOT NULL,  
<br/>niveau_maitrise niveau_maitrise_enum NOT NULL,  
<br/>CONSTRAINT fk_maitrise_user  
FOREIGN KEY (utilisateur_id)  
REFERENCES utilisateur(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT fk_maitrise_domaine  
FOREIGN KEY (domaine_id)  
REFERENCES domaine(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT uq_maitrise  
UNIQUE(utilisateur_id, domaine_id)  
);  

# 6\. Besoins

CREATE TABLE besoin (  
id BIGSERIAL PRIMARY KEY,  
<br/>utilisateur_id BIGINT NOT NULL,  
domaine_id BIGINT NOT NULL,  
<br/>niveau_priorite SMALLINT NOT NULL  
CHECK (niveau_priorite BETWEEN 1 AND 5),  
<br/>CONSTRAINT fk_besoin_user  
FOREIGN KEY (utilisateur_id)  
REFERENCES utilisateur(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT fk_besoin_domaine  
FOREIGN KEY (domaine_id)  
REFERENCES domaine(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT uq_besoin  
UNIQUE(utilisateur_id, domaine_id)  
);  

# 7\. Publications

CREATE TABLE publication (  
id BIGSERIAL PRIMARY KEY,  
<br/>auteur_id BIGINT NOT NULL,  
<br/>type_publication type_publication_enum NOT NULL,  
<br/>titre VARCHAR(255) NOT NULL,  
<br/>description TEXT NOT NULL,  
<br/>mode_mentorat mode_mentorat_enum NOT NULL,  
<br/>statut statut_publication_enum NOT NULL DEFAULT 'OUVERTE',  
<br/>created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
<br/>CONSTRAINT fk_publication_auteur  
FOREIGN KEY (auteur_id)  
REFERENCES utilisateur(id)  
ON DELETE CASCADE  
);  

# 8\. Publication domaine

CREATE TABLE publication_domaine (  
id BIGSERIAL PRIMARY KEY,  
<br/>publication_id BIGINT NOT NULL,  
domaine_id BIGINT NOT NULL,  
<br/>statut_couverture statut_couverture_enum  
NOT NULL DEFAULT 'OUVERT',  
<br/>CONSTRAINT fk_pub_dom_publication  
FOREIGN KEY (publication_id)  
REFERENCES publication(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT fk_pub_dom_domaine  
FOREIGN KEY (domaine_id)  
REFERENCES domaine(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT uq_pub_domaine  
UNIQUE(publication_id, domaine_id)  
);  

# 9\. Disponibilités publication

CREATE TABLE disponibilite_publication (  
id BIGSERIAL PRIMARY KEY,  
<br/>publication_id BIGINT NOT NULL,  
<br/>jour_semaine SMALLINT NOT NULL  
CHECK (jour_semaine BETWEEN 1 AND 7),  
<br/>heure_debut TIME NOT NULL,  
heure_fin TIME NOT NULL,  
<br/>CONSTRAINT fk_dispo_publication  
FOREIGN KEY (publication_id)  
REFERENCES publication(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT chk_dispo_pub_heure  
CHECK (heure_fin > heure_debut)  
);  

# 10\. Réponses

CREATE TABLE reponse (  
id BIGSERIAL PRIMARY KEY,  
<br/>publication_id BIGINT NOT NULL,  
auteur_id BIGINT NOT NULL,  
<br/>message TEXT,  
<br/>statut statut_reponse_enum  
NOT NULL DEFAULT 'EN_ATTENTE',  
<br/>created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
<br/>CONSTRAINT fk_reponse_publication  
FOREIGN KEY (publication_id)  
REFERENCES publication(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT fk_reponse_auteur  
FOREIGN KEY (auteur_id)  
REFERENCES utilisateur(id)  
ON DELETE CASCADE  
);  

# 11\. Réponse domaine

CREATE TABLE reponse_domaine (  
id BIGSERIAL PRIMARY KEY,  
<br/>reponse_id BIGINT NOT NULL,  
domaine_id BIGINT NOT NULL,  
<br/>CONSTRAINT fk_rep_dom_reponse  
FOREIGN KEY (reponse_id)  
REFERENCES reponse(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT fk_rep_dom_domaine  
FOREIGN KEY (domaine_id)  
REFERENCES domaine(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT uq_reponse_domaine  
UNIQUE(reponse_id, domaine_id)  
);  

# 12\. Relation mentorat

CREATE TABLE relation_mentorat (  
id BIGSERIAL PRIMARY KEY,  
<br/>mentor_id BIGINT NOT NULL,  
mentore_id BIGINT NOT NULL,  
<br/>reponse_id BIGINT NOT NULL UNIQUE,  
<br/>statut statut_relation_enum  
NOT NULL DEFAULT 'ACTIVE',  
<br/>date_debut TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
<br/>date_fin TIMESTAMP,  
<br/>commentaire_fin TEXT,  
<br/>CONSTRAINT fk_relation_mentor  
FOREIGN KEY (mentor_id)  
REFERENCES utilisateur(id),  
<br/>CONSTRAINT fk_relation_mentore  
FOREIGN KEY (mentore_id)  
REFERENCES utilisateur(id),  
<br/>CONSTRAINT fk_relation_reponse  
FOREIGN KEY (reponse_id)  
REFERENCES reponse(id),  
<br/>CONSTRAINT chk_relation_personnes  
CHECK (mentor_id <> mentore_id)  
);  

# 13\. Relation domaine

CREATE TABLE relation_domaine (  
id BIGSERIAL PRIMARY KEY,  
<br/>relation_id BIGINT NOT NULL,  
domaine_id BIGINT NOT NULL,  
<br/>statut statut_relation_domaine_enum  
NOT NULL DEFAULT 'EN_COURS',  
<br/>CONSTRAINT fk_rel_dom_relation  
FOREIGN KEY (relation_id)  
REFERENCES relation_mentorat(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT fk_rel_dom_domaine  
FOREIGN KEY (domaine_id)  
REFERENCES domaine(id),  
<br/>CONSTRAINT uq_relation_domaine  
UNIQUE(relation_id, domaine_id)  
);  

# 14\. Conversation

CREATE TABLE conversation (  
id BIGSERIAL PRIMARY KEY,  
<br/>relation_id BIGINT NOT NULL UNIQUE,  
<br/>created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
<br/>CONSTRAINT fk_conversation_relation  
FOREIGN KEY (relation_id)  
REFERENCES relation_mentorat(id)  
ON DELETE CASCADE  
);  

# 15\. Messages

CREATE TABLE message (  
id BIGSERIAL PRIMARY KEY,  
<br/>conversation_id BIGINT NOT NULL,  
expediteur_id BIGINT NOT NULL,  
<br/>contenu TEXT NOT NULL,  
<br/>lu BOOLEAN NOT NULL DEFAULT FALSE,  
<br/>created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
<br/>CONSTRAINT fk_message_conversation  
FOREIGN KEY (conversation_id)  
REFERENCES conversation(id)  
ON DELETE CASCADE,  
<br/>CONSTRAINT fk_message_expediteur  
FOREIGN KEY (expediteur_id)  
REFERENCES utilisateur(id)  
);  

# 16\. Notifications

CREATE TABLE notification (  
id BIGSERIAL PRIMARY KEY,  
<br/>utilisateur_id BIGINT NOT NULL,  
<br/>type_notification VARCHAR(50) NOT NULL,  
<br/>contenu TEXT NOT NULL,  
<br/>lu BOOLEAN NOT NULL DEFAULT FALSE,  
<br/>created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  
<br/>CONSTRAINT fk_notification_utilisateur  
FOREIGN KEY (utilisateur_id)  
REFERENCES utilisateur(id)  
ON DELETE CASCADE  
);  

# 17\. Index de performance

CREATE INDEX idx_publication_statut  
ON publication(statut);  
<br/>CREATE INDEX idx_publication_type  
ON publication(type_publication);  
<br/>CREATE INDEX idx_publication_auteur  
ON publication(auteur_id);  
<br/>CREATE INDEX idx_reponse_publication  
ON reponse(publication_id);  
<br/>CREATE INDEX idx_reponse_auteur  
ON reponse(auteur_id);  
<br/>CREATE INDEX idx_message_conversation  
ON message(conversation_id);  
<br/>CREATE INDEX idx_notification_utilisateur  
ON notification(utilisateur_id);  
<br/>CREATE INDEX idx_relation_mentor  
ON relation_mentorat(mentor_id);  
<br/>CREATE INDEX idx_relation_mentore  
ON relation_mentorat(mentore_id);  
<br/>CREATE INDEX idx_domaine_nom  
ON domaine(nom);