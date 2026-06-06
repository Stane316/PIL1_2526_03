-- ============================================================
-- IFRI MentorLink — Schéma Physique PostgreSQL
-- Version 1.0
-- ============================================================

-- ------------------------------------------------------------
-- 0. Nettoyage (optionnel, utile en redéploiement)
-- ------------------------------------------------------------

DROP TABLE IF EXISTS notification CASCADE;
DROP TABLE IF EXISTS message CASCADE;
DROP TABLE IF EXISTS conversation CASCADE;
DROP TABLE IF EXISTS relation_domaine CASCADE;
DROP TABLE IF EXISTS relation_mentorat CASCADE;
DROP TABLE IF EXISTS reponse_domaine CASCADE;
DROP TABLE IF EXISTS reponse CASCADE;
DROP TABLE IF EXISTS disponibilite_publication CASCADE;
DROP TABLE IF EXISTS publication_domaine CASCADE;
DROP TABLE IF EXISTS publication CASCADE;
DROP TABLE IF EXISTS besoin CASCADE;
DROP TABLE IF EXISTS maitrise CASCADE;
DROP TABLE IF EXISTS disponibilite_utilisateur CASCADE;
DROP TABLE IF EXISTS domaine CASCADE;
DROP TABLE IF EXISTS utilisateur CASCADE;

DROP TYPE IF EXISTS filiere_enum CASCADE;
DROP TYPE IF EXISTS niveau_enum CASCADE;
DROP TYPE IF EXISTS niveau_maitrise_enum CASCADE;
DROP TYPE IF EXISTS type_publication_enum CASCADE;
DROP TYPE IF EXISTS mode_mentorat_enum CASCADE;
DROP TYPE IF EXISTS statut_publication_enum CASCADE;
DROP TYPE IF EXISTS statut_reponse_enum CASCADE;
DROP TYPE IF EXISTS statut_relation_enum CASCADE;
DROP TYPE IF EXISTS statut_couverture_enum CASCADE;
DROP TYPE IF EXISTS statut_relation_domaine_enum CASCADE;


-- ============================================================
-- 1. Types ENUM
-- ============================================================

CREATE TYPE filiere_enum AS ENUM (
    'GL',
    'IA',
    'SEIOT',
    'CYBERSECURITE',
    'IM'
);

CREATE TYPE niveau_enum AS ENUM (
    'LICENCE_1',
    'LICENCE_2',
    'LICENCE_3'
);

CREATE TYPE niveau_maitrise_enum AS ENUM (
    'DEBUTANT',
    'INTERMEDIAIRE',
    'AVANCE'
);

CREATE TYPE type_publication_enum AS ENUM (
    'OFFRE',
    'DEMANDE'
);

CREATE TYPE mode_mentorat_enum AS ENUM (
    'PRESENTIEL',
    'EN_LIGNE',
    'HYBRIDE'
);

CREATE TYPE statut_publication_enum AS ENUM (
    'OUVERTE',
    'FERMEE',
    'ARCHIVEE'
);

CREATE TYPE statut_reponse_enum AS ENUM (
    'EN_ATTENTE',
    'ACCEPTEE',
    'REFUSEE'
);

CREATE TYPE statut_relation_enum AS ENUM (
    'ACTIVE',
    'SUSPENDUE',
    'TERMINEE'
);

CREATE TYPE statut_couverture_enum AS ENUM (
    'OUVERT',
    'COUVERT',
    'ABANDONNE'
);

CREATE TYPE statut_relation_domaine_enum AS ENUM (
    'EN_COURS',
    'MAITRISE',
    'ABANDONNE'
);


-- ============================================================
-- 2. Table utilisateur
-- ============================================================

CREATE TABLE utilisateur (
    id            BIGSERIAL       PRIMARY KEY,

    nom           VARCHAR(100)    NOT NULL,
    prenom        VARCHAR(100)    NOT NULL,

    email         VARCHAR(255)    NOT NULL UNIQUE,
    telephone     VARCHAR(30)     NOT NULL UNIQUE,

    password_hash VARCHAR(255)    NOT NULL,

    photo_profil  TEXT,           -- chemin vers le fichier uploadé

    bio           TEXT,

    filiere       filiere_enum    NOT NULL,
    niveau        niveau_enum     NOT NULL,

    actif         BOOLEAN         NOT NULL DEFAULT TRUE,

    created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 3. Table domaine
-- ============================================================

CREATE TABLE domaine (
    id          BIGSERIAL       PRIMARY KEY,

    nom         VARCHAR(150)    NOT NULL UNIQUE,

    description TEXT,

    valide      BOOLEAN         NOT NULL DEFAULT TRUE,

    created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 4. Disponibilités utilisateur
-- ============================================================

CREATE TABLE disponibilite_utilisateur (
    id              BIGSERIAL   PRIMARY KEY,

    utilisateur_id  BIGINT      NOT NULL,

    jour_semaine    SMALLINT    NOT NULL
                                CHECK (jour_semaine BETWEEN 1 AND 7),

    heure_debut     TIME        NOT NULL,
    heure_fin       TIME        NOT NULL,

    CONSTRAINT fk_dispo_user
        FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateur(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_dispo_user_heure
        CHECK (heure_fin > heure_debut)
);


-- ============================================================
-- 5. Maîtrises
-- ============================================================

CREATE TABLE maitrise (
    id               BIGSERIAL              PRIMARY KEY,

    utilisateur_id   BIGINT                 NOT NULL,
    domaine_id       BIGINT                 NOT NULL,

    niveau_maitrise  niveau_maitrise_enum   NOT NULL,

    CONSTRAINT fk_maitrise_user
        FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateur(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_maitrise_domaine
        FOREIGN KEY (domaine_id)
        REFERENCES domaine(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_maitrise
        UNIQUE (utilisateur_id, domaine_id)
);


-- ============================================================
-- 6. Besoins
-- ============================================================

CREATE TABLE besoin (
    id               BIGSERIAL   PRIMARY KEY,

    utilisateur_id   BIGINT      NOT NULL,
    domaine_id       BIGINT      NOT NULL,

    niveau_priorite  SMALLINT    NOT NULL
                                 CHECK (niveau_priorite BETWEEN 1 AND 5),

    CONSTRAINT fk_besoin_user
        FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateur(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_besoin_domaine
        FOREIGN KEY (domaine_id)
        REFERENCES domaine(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_besoin
        UNIQUE (utilisateur_id, domaine_id)
);


-- ============================================================
-- 7. Publications
-- ============================================================

CREATE TABLE publication (
    id                BIGSERIAL                PRIMARY KEY,

    auteur_id         BIGINT                   NOT NULL,

    type_publication  type_publication_enum    NOT NULL,

    titre             VARCHAR(255)             NOT NULL,

    description       TEXT                     NOT NULL,

    mode_mentorat     mode_mentorat_enum       NOT NULL,

    statut            statut_publication_enum  NOT NULL DEFAULT 'OUVERTE',

    created_at        TIMESTAMP                NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP                NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_publication_auteur
        FOREIGN KEY (auteur_id)
        REFERENCES utilisateur(id)
        ON DELETE CASCADE
);


-- ============================================================
-- 8. Publication — Domaines couverts
-- ============================================================

CREATE TABLE publication_domaine (
    id                 BIGSERIAL               PRIMARY KEY,

    publication_id     BIGINT                  NOT NULL,
    domaine_id         BIGINT                  NOT NULL,

    statut_couverture  statut_couverture_enum  NOT NULL DEFAULT 'OUVERT',

    CONSTRAINT fk_pub_dom_publication
        FOREIGN KEY (publication_id)
        REFERENCES publication(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_pub_dom_domaine
        FOREIGN KEY (domaine_id)
        REFERENCES domaine(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_pub_domaine
        UNIQUE (publication_id, domaine_id)
);


-- ============================================================
-- 9. Disponibilités d'une publication
-- ============================================================

CREATE TABLE disponibilite_publication (
    id              BIGSERIAL   PRIMARY KEY,

    publication_id  BIGINT      NOT NULL,

    jour_semaine    SMALLINT    NOT NULL
                                CHECK (jour_semaine BETWEEN 1 AND 7),

    heure_debut     TIME        NOT NULL,
    heure_fin       TIME        NOT NULL,

    CONSTRAINT fk_dispo_publication
        FOREIGN KEY (publication_id)
        REFERENCES publication(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_dispo_pub_heure
        CHECK (heure_fin > heure_debut)
);


-- ============================================================
-- 10. Réponses à une publication
-- ============================================================

CREATE TABLE reponse (
    id              BIGSERIAL              PRIMARY KEY,

    publication_id  BIGINT                 NOT NULL,
    auteur_id       BIGINT                 NOT NULL,

    message         TEXT,

    statut          statut_reponse_enum    NOT NULL DEFAULT 'EN_ATTENTE',

    created_at      TIMESTAMP              NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reponse_publication
        FOREIGN KEY (publication_id)
        REFERENCES publication(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_reponse_auteur
        FOREIGN KEY (auteur_id)
        REFERENCES utilisateur(id)
        ON DELETE CASCADE
);


-- ============================================================
-- 11. Réponse — Domaines concernés
-- ============================================================

CREATE TABLE reponse_domaine (
    id          BIGSERIAL   PRIMARY KEY,

    reponse_id  BIGINT      NOT NULL,
    domaine_id  BIGINT      NOT NULL,

    CONSTRAINT fk_rep_dom_reponse
        FOREIGN KEY (reponse_id)
        REFERENCES reponse(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_rep_dom_domaine
        FOREIGN KEY (domaine_id)
        REFERENCES domaine(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_reponse_domaine
        UNIQUE (reponse_id, domaine_id)
);


-- ============================================================
-- 12. Relation de mentorat
-- ============================================================

CREATE TABLE relation_mentorat (
    id               BIGSERIAL              PRIMARY KEY,

    mentor_id        BIGINT                 NOT NULL,
    mentore_id       BIGINT                 NOT NULL,

    reponse_id       BIGINT                 NOT NULL UNIQUE,

    statut           statut_relation_enum   NOT NULL DEFAULT 'ACTIVE',

    date_debut       TIMESTAMP              NOT NULL DEFAULT CURRENT_TIMESTAMP,

    date_fin         TIMESTAMP,

    commentaire_fin  TEXT,

    CONSTRAINT fk_relation_mentor
        FOREIGN KEY (mentor_id)
        REFERENCES utilisateur(id),

    CONSTRAINT fk_relation_mentore
        FOREIGN KEY (mentore_id)
        REFERENCES utilisateur(id),

    CONSTRAINT fk_relation_reponse
        FOREIGN KEY (reponse_id)
        REFERENCES reponse(id),

    CONSTRAINT chk_relation_personnes
        CHECK (mentor_id <> mentore_id)
);


-- ============================================================
-- 13. Relation — Domaines travaillés
-- ============================================================

CREATE TABLE relation_domaine (
    id           BIGSERIAL                      PRIMARY KEY,

    relation_id  BIGINT                         NOT NULL,
    domaine_id   BIGINT                         NOT NULL,

    statut       statut_relation_domaine_enum   NOT NULL DEFAULT 'EN_COURS',

    CONSTRAINT fk_rel_dom_relation
        FOREIGN KEY (relation_id)
        REFERENCES relation_mentorat(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_rel_dom_domaine
        FOREIGN KEY (domaine_id)
        REFERENCES domaine(id),

    CONSTRAINT uq_relation_domaine
        UNIQUE (relation_id, domaine_id)
);


-- ============================================================
-- 14. Conversation
-- ============================================================

CREATE TABLE conversation (
    id           BIGSERIAL   PRIMARY KEY,

    relation_id  BIGINT      NOT NULL UNIQUE,

    created_at   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_conversation_relation
        FOREIGN KEY (relation_id)
        REFERENCES relation_mentorat(id)
        ON DELETE CASCADE
);


-- ============================================================
-- 15. Messages
-- ============================================================

CREATE TABLE message (
    id               BIGSERIAL   PRIMARY KEY,

    conversation_id  BIGINT      NOT NULL,
    expediteur_id    BIGINT      NOT NULL,

    contenu          TEXT        NOT NULL,

    lu               BOOLEAN     NOT NULL DEFAULT FALSE,

    created_at       TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_message_conversation
        FOREIGN KEY (conversation_id)
        REFERENCES conversation(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_message_expediteur
        FOREIGN KEY (expediteur_id)
        REFERENCES utilisateur(id)
);


-- ============================================================
-- 16. Notifications
-- ============================================================

CREATE TABLE notification (
    id                  BIGSERIAL       PRIMARY KEY,

    utilisateur_id      BIGINT          NOT NULL,

    type_notification   VARCHAR(50)     NOT NULL,

    contenu             TEXT            NOT NULL,

    lu                  BOOLEAN         NOT NULL DEFAULT FALSE,

    created_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_notification_utilisateur
        FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateur(id)
        ON DELETE CASCADE
);


-- ============================================================
-- 17. Index de performance
-- ============================================================

CREATE INDEX idx_publication_statut
    ON publication(statut);

CREATE INDEX idx_publication_type
    ON publication(type_publication);

CREATE INDEX idx_publication_auteur
    ON publication(auteur_id);

CREATE INDEX idx_reponse_publication
    ON reponse(publication_id);

CREATE INDEX idx_reponse_auteur
    ON reponse(auteur_id);

CREATE INDEX idx_message_conversation
    ON message(conversation_id);

CREATE INDEX idx_notification_utilisateur
    ON notification(utilisateur_id);

CREATE INDEX idx_relation_mentor
    ON relation_mentorat(mentor_id);

CREATE INDEX idx_relation_mentore
    ON relation_mentorat(mentore_id);

CREATE INDEX idx_domaine_nom
    ON domaine(nom);


-- ============================================================
-- FIN DU SCRIPT
-- ============================================================