-- =========================================================================
-- GENERATION MASSIVE DE 102 UTILISATEURS (BROUILLAGE ALGORITHMIQUE)
-- =========================================================================

-- 1. Insertion des profils dans la table 'utilisateur'
INSERT INTO utilisateur (id, nom, prenom, email, telephone, password_hash, bio, filiere, niveau)
SELECT 
    i,
    CASE 
        WHEN i % 6 = 0 THEN 'Bio' WHEN i % 6 = 1 THEN 'Koffi' WHEN i % 6 = 2 THEN 'Sanni' 
        WHEN i % 6 = 3 THEN 'Agossou' WHEN i % 6 = 4 THEN 'Bello' ELSE 'Houngbedji' 
    END || ' ' || i,
    CASE 
        WHEN i % 5 = 0 THEN 'Arnaud' WHEN i % 5 = 1 THEN 'Clarisse' WHEN i % 5 = 2 THEN 'Frédéric' 
        WHEN i % 5 = 3 THEN 'Inès' ELSE 'Farid' 
    END,
    'etudiant' || i || '@mentorlink.ifri.bj',
    '+229 97000' || LPAD(i::text, 3, '0'),
    'pbkdf2_sha256$800000$fakehash$',
    'Étudiant passionné participant au programme de mentorat IFRI-MentorLink.',
    -- Répartition homogène des filières
    CASE (i % 5) 
        WHEN 0 THEN 'GL'::filiere_enum WHEN 1 THEN 'IA'::filiere_enum 
        WHEN 2 THEN 'CYBERSECURITE'::filiere_enum WHEN 3 THEN 'SEIOT'::filiere_enum 
        ELSE 'IM'::filiere_enum 
    END,
    -- Répartition homogène des niveaux
    CASE (i % 3) 
        WHEN 0 THEN 'LICENCE_1'::niveau_enum 
        WHEN 1 THEN 'LICENCE_2'::niveau_enum 
        ELSE 'LICENCE_3'::niveau_enum 
    END
FROM generate_series(1, 102) AS i;

-- 2. Injection de MAÎTRISES (Points forts) pour le brouillage
-- Chaque étudiant se voit attribuer de 1 à 3 maîtrises parmi les 90 domaines de l'IFRI
INSERT INTO maitrise (utilisateur_id, domaine_id, niveau_maitrise)
SELECT 
    u.id,
    d.id,
    CASE WHEN (u.id + d.id) % 3 = 0 THEN 'DEBUTANT'::niveau_maitrise_enum 
         WHEN (u.id + d.id) % 3 = 1 THEN 'INTERMEDIAIRE'::niveau_maitrise_enum 
         ELSE 'AVANCE'::niveau_maitrise_enum 
    END
FROM utilisateur u
CROSS JOIN (
    -- On cible des IDs de domaines variés répartis dans le script de base
    SELECT id FROM domaine WHERE id IN (1, 2, 3, 7, 11, 19, 20, 26, 27, 34, 43, 49, 54, 62, 68, 77)
) d
-- Condition de dispersion pour éviter que tout le monde ait les mêmes matières
WHERE (u.id * d.id) % 7 IN (1, 3)
ON CONFLICT (utilisateur_id, domaine_id) DO NOTHING;

-- 3. Injection de BESOINS (Points faibles) pour le brouillage
-- Chaque étudiant reçoit des besoins sur des matières différentes de ses maîtrises
INSERT INTO besoin (utilisateur_id, domaine_id, niveau_priorite)
SELECT 
    u.id,
    d.id,
    ((u.id + d.id) % 5) + 1 -- Priorité de 1 à 5
FROM utilisateur u
CROSS JOIN (
    SELECT id FROM domaine WHERE id IN (1, 2, 3, 7, 11, 19, 20, 26, 27, 34, 43, 49, 54, 62, 68, 77)
) d
WHERE (u.id * d.id) % 9 IN (2, 4) 
  -- Sécurité : un utilisateur ne peut pas avoir un besoin là où il a déjà une maîtrise
  AND NOT EXISTS (
      SELECT 1 FROM maitrise m WHERE m.utilisateur_id = u.id AND m.domaine_id = d.id
  )
ON CONFLICT (utilisateur_id, domaine_id) DO NOTHING;

-- 4. RECALAGE DE SECURITE DES AUTO-INCREMENTS
SELECT setval('auth_user_id_seq', (SELECT MAX(id) FROM auth_user));
SELECT setval('utilisateur_id_seq', (SELECT MAX(id) FROM utilisateur));