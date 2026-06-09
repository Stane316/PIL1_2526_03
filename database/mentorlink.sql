-- ============================================================
-- IFRI MentorLink — Schéma Physique PostgreSQL
-- Version 1.0
-- ============================================================

-- ------------------------------------------------------------
-- 0. Nettoyage (optionnel, utile en redéploiement)
-- ------------------------------------------------------------
TRUNCATE TABLE auth_user CASCADE;
COMMIT;
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

SELECT * FROM public.auth_user;




-- ============================================================
-- IFRI MentorLink — Données initiales : table domaine
-- ============================================================
-- À exécuter après mentorlink.sql
-- Couvre toutes les filières : GL, IA, IM, SE&IoT, Cybersécurité
-- ============================================================

INSERT INTO domaine (nom, description) VALUES

-- ============================================================
-- 1. MATHÉMATIQUES FONDAMENTALES
-- ============================================================
('Logique mathématique',          'Calcul des prédicats, logique propositionnelle, démonstrations formelles'),
('Théorie des ensembles',         'Ensembles, relations, fonctions, cardinalité'),
('Algèbre linéaire',              'Vecteurs, matrices, déterminants, espaces vectoriels'),
('Algèbre abstraite',             'Groupes, anneaux, corps, morphismes'),
('Arithmétique & théorie des nombres', 'Divisibilité, modularité, nombres premiers, PGCD'),
('Analyse mathématique',          'Limites, dérivées, intégrales, suites et séries'),
('Mathématiques discrètes',       'Combinatoire, graphes, dénombrement, relations de récurrence'),
('Probabilités',                  'Espaces de probabilité, variables aléatoires, lois classiques'),
('Statistiques descriptives',     'Moyenne, variance, médiane, représentations graphiques'),
('Statistiques inférentielles',   'Tests d hypothèse, intervalles de confiance, p-valeur'),

-- ============================================================
-- 2. MATHÉMATIQUES APPLIQUÉES À L'INFORMATIQUE
-- ============================================================
('Théorie des graphes',           'Graphes orientés/non orientés, arbres, parcours, algorithmes classiques (Dijkstra, Kruskal)'),
('Théorie des automates',         'Automates finis, expressions régulières, langages formels'),
('Cryptographie mathématique',    'RSA, courbes elliptiques, fonctions de hachage, protocoles'),
('Optimisation mathématique',     'Programmation linéaire, gradient, méthode du simplex'),
('Algèbre de Boole',              'Opérateurs logiques, simplification, tables de vérité, circuits'),
('Mathématiques pour le ML',      'Gradient, dérivées partielles, régression, matrices de covariance'),
('Théorie de l information',      'Entropie, codage, compression, capacité de canal'),
('Analyse numérique',             'Méthodes d approximation, interpolation, résolution numérique'),

-- ============================================================
-- 3. ALGORITHMIQUE & PROGRAMMATION
-- ============================================================
('Algorithmique de base',         'Notions de complexité, structures de contrôle, pseudo-code'),
('Structures de données',         'Tableaux, listes, piles, files, arbres, tas, graphes'),
('Algorithmes de tri & recherche','Tri rapide, fusion, insertion, recherche binaire'),
('Récursivité',                   'Fonctions récursives, backtracking, divide and conquer'),
('Programmation dynamique',       'Memoïsation, sous-problèmes optimaux, sac à dos, LCS'),
('Programmation orientée objet',  'Classes, héritage, polymorphisme, encapsulation, design patterns'),
('Programmation fonctionnelle',   'Fonctions pures, immutabilité, récursion, map/filter/reduce'),
('Programmation Python',          'Syntaxe, structures, bibliothèques standard, fichiers, modules'),
('Programmation C / C++',         'Pointeurs, gestion mémoire, structures, compilation'),
('Programmation Java',            'JVM, Collections, exceptions, interfaces, Maven'),
('Programmation JavaScript',      'DOM, événements, closures, ES6+, asynchrone'),
('Programmation PHP',             'Syntaxe, sessions, formulaires, interaction base de données'),

-- ============================================================
-- 4. DÉVELOPPEMENT WEB & MOBILE
-- ============================================================
('HTML & CSS',                    'Structure de page, mise en forme, responsive design'),
('JavaScript avancé',             'Promises, async/await, fetch, modules ES6'),
('Frameworks frontend',           'React, Vue.js, Angular — composants, état, routing'),
('Frameworks backend Python',     'Django, Flask — routes, modèles, vues, ORM'),
('Frameworks backend Node.js',    'Express.js — middlewares, REST API, authentification'),
('API REST',                      'Conception d API, verbes HTTP, JSON, stateless, documentation'),
('Développement mobile',          'React Native, Flutter, Android natif — interfaces et navigation'),
('Tailwind CSS',                  'Utilitaires CSS, responsive, thèmes, composants'),

-- ============================================================
-- 5. BASES DE DONNÉES
-- ============================================================
('Modélisation de bases de données','MCD, MPD, normalisation, dépendances fonctionnelles'),
('Algèbre relationnelle',         'Sélection, projection, jointures, union, intersection'),
('Langage SQL',                   'DDL, DML, DQL — CREATE, SELECT, JOIN, GROUP BY, sous-requêtes'),
('PostgreSQL',                    'Types avancés, ENUM, index, transactions, extensions'),
('MySQL',                         'Configuration, requêtes, gestion des utilisateurs, optimisation'),
('Bases de données NoSQL',        'MongoDB, Redis, Cassandra — documents, clés-valeurs, colonnes'),
('Optimisation SQL',              'Index, plans d exécution, requêtes performantes'),

-- ============================================================
-- 6. SYSTÈMES & RÉSEAUX
-- ============================================================
('Systèmes d exploitation',       'Processus, mémoire virtuelle, système de fichiers, ordonnancement'),
('Administration Linux',          'Commandes shell, droits, services, cron, gestion de paquets'),
('Scripting Bash',                'Automatisation, variables, boucles, conditions, pipes'),
('Réseaux informatiques',         'Modèle OSI/TCP-IP, adressage IP, routage, protocoles'),
('Administration réseau',         'Configuration routeurs/switches, VLAN, NAT, DNS, DHCP'),
('Protocoles applicatifs',        'HTTP, HTTPS, FTP, SMTP, SSH, WebSocket'),
('Virtualisation & conteneurs',   'VirtualBox, VMware, Docker, Docker Compose'),

-- ============================================================
-- 7. INTELLIGENCE ARTIFICIELLE & DATA
-- ============================================================
('Machine Learning',              'Régression, classification, clustering, évaluation de modèles'),
('Deep Learning',                 'Réseaux de neurones, CNN, RNN, LSTM, frameworks Keras/PyTorch'),
('Traitement du langage naturel', 'Tokenisation, embeddings, transformers, NLP avec Python'),
('Vision par ordinateur',         'Traitement d images, détection d objets, OpenCV'),
('Science des données',           'Pandas, NumPy, visualisation, nettoyage, exploration de données'),
('Visualisation de données',      'Matplotlib, Seaborn, Plotly, dashboards, graphiques'),
('Big Data',                      'Hadoop, Spark, traitement distribué de grands volumes'),

-- ============================================================
-- 8. CYBERSÉCURITÉ
-- ============================================================
('Sécurité des systèmes',         'Vulnérabilités OS, durcissement, gestion des droits'),
('Sécurité des réseaux',          'Firewalls, VPN, IDS/IPS, analyse de trafic'),
('Sécurité des applications web', 'OWASP Top 10, injections SQL, XSS, CSRF, authentification'),
('Cryptographie appliquée',       'Chiffrement symétrique/asymétrique, TLS, certificats'),
('Ethical hacking',               'Tests de pénétration, reconnaissance, exploitation, rapports'),
('Forensique numérique',          'Analyse post-incident, récupération de données, logs'),
('Sécurité des objets connectés', 'Protocoles IoT, firmware, vecteurs d attaque embarqués'),

-- ============================================================
-- 9. SYSTÈMES EMBARQUÉS & IoT
-- ============================================================
('Électronique numérique',        'Portes logiques, circuits combinatoires/séquentiels, FPGA'),
('Microcontrôleurs',              'Arduino, STM32, ESP32 — programmation bas niveau'),
('Systèmes embarqués Linux',      'Raspberry Pi, Buildroot, drivers, temps réel'),
('Protocoles IoT',                'MQTT, CoAP, Zigbee, LoRa, communication sans fil'),
('Systèmes temps réel (RTOS)',    'FreeRTOS, tâches, interruptions, gestion de ressources'),
('Conception de PCB',             'KiCad, schématique, routage, fabrication'),

-- ============================================================
-- 10. GÉNIE LOGICIEL & MÉTHODES
-- ============================================================
('Génie logiciel',                'Cycle de vie logiciel, qualité, tests, maintenance'),
('UML & modélisation',            'Diagrammes de classes, séquences, cas d utilisation, activités'),
('Méthodes agiles',               'Scrum, Kanban, sprints, user stories, rétrospectives'),
('Tests logiciels',               'Tests unitaires, d intégration, TDD, couverture de code'),
('Gestion de version Git',        'Commits, branches, merge, rebase, GitHub/GitLab, PRs'),
('Architecture logicielle',       'MVC, microservices, API Gateway, event-driven, clean architecture'),
('DevOps & CI/CD',                'GitHub Actions, pipelines, déploiement automatisé, monitoring'),
('Gestion de projet informatique','Planification, WBS, gestion des risques, suivi'),

-- ============================================================
-- 11. INFORMATIQUE THÉORIQUE
-- ============================================================
('Théorie de la calculabilité',   'Machine de Turing, décidabilité, problème de l arrêt'),
('Complexité algorithmique',      'Classes P, NP, NP-complet, réductions'),
('Compilation',                   'Analyse lexicale, syntaxique, génération de code, optimisation'),
('Systèmes de types',             'Typage statique/dynamique, inférence, polymorphisme paramétrique'),
('Langages formels',              'Grammaires de Chomsky, automates, expressions rationnelles'),

-- ============================================================
-- 12. LANGUES & COMMUNICATION
-- ============================================================
('Anglais technique',             'Lecture de documentation, rédaction de rapports, vocabulaire IT'),
('Anglais général',               'Expression orale, grammaire, compréhension, TOEIC/IELTS'),
('Français professionnel',        'Rédaction de rapports, mails formels, compte-rendus'),
('Communication orale',           'Prise de parole, présentations, argumentation'),
('Rédaction technique',           'Documentation, README, spécifications, cahier des charges'),

-- ============================================================
-- 13. OUTILS & ENVIRONNEMENTS
-- ============================================================
('Environnement de développement','VS Code, IntelliJ, configuration, extensions, debugging'),
('Linux & terminal',              'Navigation, fichiers, processus, éditeurs vim/nano'),
('Outils de collaboration',       'Trello, Notion, Slack, gestion de tâches en équipe'),
('Suite bureautique',             'Word, Excel, PowerPoint — usage professionnel'),
('LaTeX',                         'Rédaction scientifique, formules, bibliographies');

-- ============================================================
-- Total : ~90 domaines
-- ============================================================
-- 1. On insère l'utilisateur de base dans la table d'authentification de Django (ID = 1)
INSERT INTO auth_user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES (1, 'pbkdf2_sha256$800000$fakehash$', false, 'dev_test', 'Mon', 'Profil', 'test@ifri.bj', false, true, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- 2. On insère son profil lié dans ta table utilisateur (en utilisant les colonnes réelles de ton .sql)
INSERT INTO utilisateur (id, filiere, niveau, telephone, bio, statut_couverture)
VALUES (1, 'GL', 'LICENCE_3', '+229 90909090', 'Développeur backend IFRI', 'DISPONIBLE')
ON CONFLICT (id) DO NOTHING;

-- 3. On insère les matières (domaines) pour que ton formulaire ne soit pas vide
INSERT INTO domaine (id, nom, description, valide) VALUES (1, 'Algorithmique', 'Bases de l''algo', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO domaine (id, nom, description, valide) VALUES (2, 'Bases de données', 'SQL et modélisation', true) ON CONFLICT (id) DO NOTHING;
INSERT INTO domaine (id, nom, description, valide) VALUES (3, 'Architecture des applications', 'Node/Django', true) ON CONFLICT (id) DO NOTHING;

-- ============================================================
-- FIN DU SCRIPT
-- ============================================================