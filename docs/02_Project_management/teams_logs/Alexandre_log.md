# IFRI MentorLinkMember Work Log Template v1

## Informations générales

**Nom du membre :NATTA YORI Alexandre**

**Rôle principal : developpement backend**

**Document :** _(Ce document retrace l’ensemble des travaux réalisés par le membre tout au long du projet IFRI MentorLink.)_

# SECTION N°1

## 1\. Informations générales

**Date :** Jeudi soir → Vendredi matin

**Heure de début :** 20h00

**Heure de fin :** 06h00

**Durée approximative :** 10 heures

**Référence de la tâche :** Mise en place du backend et du système d'authentification

**Responsable :** Alexandre

## 2\. Objectif de la tâche

Mettre en place l'architecture backend du projet IFRI MentorLink ainsi que le système complet d'authentification des utilisateurs.

## 3\. Analyse préalable

Avant de commencer le développement, il a fallu comprendre :

- L'architecture générale du projet.
- Le fonctionnement de Django.
- La gestion de l'authentification personnalisée.
- La connexion entre Django et PostgreSQL.
- La mise en place de la confirmation d'adresse e-mail et de la récupération de mot de passe.

### Documentation consultée

- Cahier des charges IFRI MentorLink
- Documentation Django
- Documentation PostgreSQL

### Vidéos / tutoriels

- https://youtu.be/M6I--B5k5wo

### Discussions avec l'équipe

- Réunion quotidienne de groupe à 18h30.
- Échanges avec Gemini concernant certaines difficultés techniques.

## 4\. Travail effectué

### Étape 1

Création de l'arborescence initiale du projet.

### Étape 2

Création de l'environnement virtuel Python.

### Étape 3

Installation des dépendances Django et PostgreSQL.

### Étape 4

Connexion du projet à la base de données PostgreSQL.

### Étape 5

Création de l'application Accounts.

### Étape 6

Configuration du dossier Core.

### Étape 7

Création des modèles d'authentification.

### Étape 8

Création des routes :

- Home
- Connexion
- Inscription
- Profil

### Étape 9

Implémentation complète :

- Inscription
- Connexion
- Déconnexion
- Confirmation d'adresse e-mail
- Réinitialisation de mot de passe

## 5\. Fichiers créés

| **Fichier** | **Description** |
| --- | --- |
| core/settings.py | Configuration générale |
| accounts/models.py | Modèles utilisateurs |
| accounts/views.py | Logique d'authentification |
| accounts/urls.py | Routes utilisateurs |
| templates/\*.html | Interfaces d'authentification |

## 6\. Fichiers modifiés

| **Fichier** | **Nature de la modification** |
| --- | --- |
| settings.py | Configuration PostgreSQL |
| urls.py | Ajout des routes |
| models.py | Ajout des modèles |

## 7\. Commandes exécutées

python -m venv venv  
<br/>venv\\Scripts\\activate  
<br/>pip install django  
<br/>pip install psycopg2-binary  
<br/>django-admin startproject core .  
<br/>python manage.py startapp accounts  
<br/>python manage.py makemigrations  
<br/>python manage.py migrate  
<br/>python manage.py runserver  
<br/>git add .  
<br/>git commit -m "Alex a mis en place la structure d'authentification"  
<br/>git push origin main

## 8\. Difficultés rencontrées

- Compréhension de l'architecture Django.
- Configuration PostgreSQL.
- Gestion des e-mails de confirmation.
- Mise en place de la récupération de mot de passe.

## 9\. Solution apportée

- Consultation de la documentation.
- Visionnage du tutoriel principal.
- Multiples essais et corrections.
- Échanges avec Gemini.

## 10\. Décisions techniques prises

- Utilisation de Django.
- Utilisation de PostgreSQL.
- Organisation du projet en applications distinctes.
- Centralisation de la configuration dans Core.

## 11\. Livrable obtenu

- Backend initial opérationnel.
- Authentification complète fonctionnelle.

## 13\. Commit Git associé

**Commit :**

Alex a mis en place la structure d'authentification

## 14\. Impact sur le projet

☑ Backend

☑ Base de données

☑ Architecture

Commentaires :

Cette tâche constitue la fondation technique de l'ensemble du projet.

## 15\. Travail restant

- Création du profil utilisateur.
- Création des fonctionnalités métier.

## 16\. Retour personnel

Cette tâche m'a permis d'approfondir ma compréhension de Django, de PostgreSQL et des mécanismes d'authentification sécurisés.

# SECTION N°2

## 1\. Informations générales

**Date :** Nuit du samedi au dimanche

**Heure de début :** 21h00

**Heure de fin :** 05h00

**Durée approximative :** 8 heures

**Référence de la tâche :** Développement du système complet de gestion du profil utilisateur

**Responsable :** Alexandre

## 2\. Objectif de la tâche

Mettre en place le système complet de profil utilisateur permettant à chaque étudiant de :

- compléter ses informations personnelles ;
- renseigner sa filière et son niveau ;
- définir ses matières fortes ;
- définir ses matières faibles ;
- ajouter une photo de profil ;
- modifier ultérieurement toutes ses informations.

Cette fonctionnalité constitue une étape essentielle du projet car elle fournit les données nécessaires aux futurs systèmes de publication et de matching.

## 3\. Analyse préalable

Avant de commencer cette tâche, il a fallu comprendre :

- la structure des modèles utilisateurs déjà mis en place ;
- la manière de relier les informations du profil à l'utilisateur authentifié ;
- la gestion des formulaires Django ;
- la gestion des fichiers images pour les photos de profil ;
- la récupération et l'affichage des données dans les templates HTML.

### Documentation consultée

- Cahier des charges IFRI MentorLink
- Documentation Django Forms
- Documentation Django Models

### Vidéos / tutoriels

- https://youtu.be/M6I--B5k5wo

### Discussions avec l'équipe

- Réunion quotidienne de synchronisation à 18h30
- Échanges avec les membres de l'équipe concernant la structure des profils

## 4\. Travail effectué

### Étape 1

Analyse des besoins du cahier des charges concernant le profil utilisateur.

### Étape 2

Vérification de la structure du modèle utilisateur déjà créée lors de la phase d'authentification.

### Étape 3

Conception de la structure des informations à enregistrer dans le profil.

### Étape 4

Création de la logique de consultation du profil dans le fichier :

profil/views.py

### Étape 5

Création de la logique de modification du profil utilisateur.

### Étape 6

Configuration des routes nécessaires dans :

profil/urls.py

### Étape 7

Création de la page :

profil.html

permettant l'affichage des informations du profil.

### Étape 8

Création du formulaire de modification :

frontend/registration/modif.html

### Étape 9

Mise en place de la gestion des informations personnelles :

- nom ;
- prénom ;
- numéro de téléphone ;
- email.

### Étape 10

Ajout de la gestion des matières maîtrisées (points forts).

### Étape 11

Ajout de la gestion des matières nécessitant de l'aide (points faibles).

### Étape 12

Implémentation de l'ajout et de la modification de la photo de profil.

### Étape 13

Tests complets de création, modification, sauvegarde et affichage des informations utilisateur.

## 5\. Fichiers créés

| **Fichier** | **Description** |
| --- | --- |
| profil.html | Affichage du profil utilisateur |
| frontend/registration/modif.html | Formulaire de modification du profil |

## 6\. Fichiers modifiés

| **Fichier** | **Nature de la modification** |
| --- | --- |
| profil/views.py | Gestion de la consultation et modification du profil |
| profil/urls.py | Ajout des routes du module profil |
| profil.html | Affichage des données utilisateur |
| frontend/registration/modif.html | Modification des informations du profil |

## 7\. Commandes exécutées

python manage.py makemigrations  
<br/>python manage.py migrate  
<br/>python manage.py runserver  
<br/>git pull origin main  
<br/>git add .  
<br/>git commit -m "depot contenant la creation complete du profil utilisateur"  
<br/>git push origin main

## 8\. Difficultés rencontrées

Aucune difficulté majeure n'a été rencontrée durant cette phase.

La structure mise en place lors de la phase d'authentification a facilité l'intégration du système de profil utilisateur.

## 9\. Solution apportée

Les rares ajustements nécessaires ont été réalisés grâce :

- aux tests locaux ;
- à la documentation Django ;
- à la réutilisation de composants déjà créés lors de la phase précédente.

## 10\. Décisions techniques prises

- Réutilisation du système d'authentification existant.
- Centralisation des informations utilisateur dans le module Profil.
- Utilisation des formulaires Django pour les modifications.
- Gestion des images via le système de médias Django.

## 11\. Livrable obtenu

Profil utilisateur entièrement fonctionnel permettant :

- la consultation des informations ;
- la modification des informations ;
- la gestion des matières fortes ;
- la gestion des matières faibles ;
- la gestion de la photo de profil.

## 12\. Vérification personnelle

☑ Le travail fonctionne correctement.

☑ La documentation est mise à jour.

☑ Les fichiers sont placés dans le bon dossier.

☑ L'architecture du projet est respectée.

☑ Le code est propre et compréhensible.

☑ Le commit Git est effectué.

☑ Le push Git est effectué.

## 13\. Commit Git associé

**Commit :**

depot contenant la creation complete du profil utilisateur

**Hash Git (optionnel) :**

Non renseigné.

## 14\. Impact sur le projet

☑ Backend

☑ Base de données

☑ Architecture

Commentaires :

Cette tâche fournit toutes les informations nécessaires au fonctionnement des futures fonctionnalités de publication d'offres, de demandes et de matching mentor-mentoré.

## 15\. Travail restant

- Création des publications de mentorat.
- Mise en place de l'algorithme de matching.
- Développement de la messagerie.

## 16\. Retour personnel

Cette tâche m'a permis d'approfondir ma compréhension :

- des formulaires Django ;
- de la gestion des fichiers médias ;
- de la liaison entre modèles et interfaces utilisateur.

La structure mise en place lors de cette phase a facilité le développement des fonctionnalités réalisées par la suite.

# SECTION N°3

## 1\. Informations générales

**Date :** Dimanche soir → Lundi

**Heure de début :** 20h00

**Heure de fin :** 01h00

**Durée approximative :** 5 heures

**Référence de la tâche :** Création des interfaces utilisateur et mise en place de la navigation générale

**Responsable :** Alexandre

## 2\. Objectif de la tâche

Créer les différentes pages HTML nécessaires au fonctionnement de l'application IFRI MentorLink et mettre en place la navigation entre celles-ci afin de préparer l'intégration des fonctionnalités métier développées par la suite.

Cette étape avait également pour objectif d'améliorer l'expérience utilisateur en fournissant une interface cohérente et intuitive.

## 3\. Analyse préalable

Avant de commencer cette tâche, il a fallu comprendre :

- l'organisation des templates Django ;
- le système d'héritage des templates ;
- la structure globale des différentes fonctionnalités du projet ;
- les besoins de navigation entre les pages ;
- les exigences du cahier des charges concernant l'expérience utilisateur.

### Documentation consultée

- Cahier des charges IFRI MentorLink
- Documentation Django Templates
- Documentation Bootstrap

### Vidéos / tutoriels

- https://youtu.be/M6I--B5k5wo

### Discussions avec l'équipe

- Réunion quotidienne de synchronisation à 18h30
- Échanges sur l'organisation générale des interfaces utilisateur
- Validation collective des pages nécessaires au projet

## 4\. Travail effectué

### Étape 1

Analyse de l'ensemble des fonctionnalités à intégrer dans l'application.

### Étape 2

Identification des pages nécessaires à la navigation générale.

### Étape 3

Organisation de l'arborescence des templates.

### Étape 4

Création du composant :

navbar.html

permettant aux utilisateurs d'accéder rapidement aux principales fonctionnalités du site.

### Étape 5

Création du composant :

header.html

permettant d'uniformiser l'en-tête de l'application.

### Étape 6

Création des pages d'accueil et de présentation.

### Étape 7

Création des pages intermédiaires nécessaires à la navigation.

### Étape 8

Ajout des liens entre les différentes interfaces.

### Étape 9

Configuration des routes permettant l'accès aux différentes pages.

### Étape 10

Vérification de la cohérence entre les liens HTML et les routes Django.

### Étape 11

Tests de navigation entre les différents modules.

### Étape 12

Correction des erreurs d'affichage détectées lors des tests.

### Étape 13

Validation finale de l'ensemble des interfaces créées.

## 5\. Fichiers créés

| **Fichier** | **Description** |
| --- | --- |
| navbar.html | Barre de navigation principale |
| header.html | En-tête commun du site |
| home.html | Page d'accueil |
| autres templates HTML | Pages secondaires de navigation |

## 6\. Fichiers modifiés

| **Fichier** | **Nature de la modification** |
| --- | --- |
| navbar.html | Création des liens de navigation |
| header.html | Uniformisation de l'interface |
| urls.py | Ajout des routes permettant l'accès aux pages |
| templates/\*.html | Création et personnalisation des interfaces |

## 7\. Commandes exécutées

python manage.py runserver  
<br/>git pull origin main  
<br/>git add .  
<br/>git commit -m "Depot des pages html"  
<br/>git push origin main

## 8\. Difficultés rencontrées

- Organisation de la navigation entre un grand nombre de pages.
- Vérification de la cohérence entre les routes Django et les liens HTML.
- Harmonisation de l'apparence générale du site.

## 9\. Solution apportée

- Mise en place d'une structure commune à toutes les pages.
- Réutilisation de composants partagés (navbar et header).
- Multiples tests de navigation.
- Validation progressive des routes.

## 10\. Décisions techniques prises

- Utilisation de composants HTML réutilisables.
- Centralisation de la navigation dans une barre de menu commune.
- Uniformisation de l'apparence de toutes les pages.
- Préparation des interfaces avant l'intégration des fonctionnalités métier.

## 11\. Livrable obtenu

Interface utilisateur complète permettant :

- l'accès aux différentes pages du projet ;
- une navigation fluide entre les modules ;
- une meilleure expérience utilisateur ;
- la préparation de l'intégration des offres, demandes, matching et messagerie.

## 12\. Vérification personnelle

☑ Le travail fonctionne correctement.

☑ La documentation est mise à jour.

☑ Les fichiers sont placés dans le bon dossier.

☑ L'architecture du projet est respectée.

☑ Le code est propre et compréhensible.

☑ Le commit Git est effectué.

☑ Le push Git est effectué.

## 13\. Commit Git associé

**Commit :**

Depot des pages html

**Hash Git (optionnel) :**

Non renseigné.

## 14\. Impact sur le projet

☑ Frontend

☑ Architecture

☑ Organisation

Commentaires :

Cette tâche a permis de construire l'ensemble de l'interface utilisateur qui servira de support aux fonctionnalités de publication, de matching et de messagerie développées par la suite.

## 15\. Travail restant

- Développement des offres et demandes de mentorat.
- Développement du système de matching.
- Développement de la messagerie.
- Intégration complète des fonctionnalités backend.

## 16\. Retour personnel

Cette tâche m'a permis de mieux comprendre l'organisation des templates Django ainsi que l'importance de concevoir une navigation claire avant d'intégrer les fonctionnalités métier.

La mise en place précoce des interfaces a facilité le développement des modules suivants en offrant un cadre visuel déjà fonctionnel.

# SECTION N°4

## 1\. Informations générales

**Date :** Lundi

**Heure de début :** 08h00

**Heure de fin :** 16h00

**Durée approximative :** 8 heures

**Référence de la tâche :** Développement du système de publications d'offres et de demandes de mentorat

**Responsable :** Alexandre

## 2\. Objectif de la tâche

Mettre en place le système permettant aux utilisateurs :

- de publier des offres de mentorat ;
- de publier des demandes de mentorat ;
- de consulter les publications disponibles ;
- de relier automatiquement les publications aux compétences enregistrées dans leur profil.

Cette fonctionnalité constitue le cœur du fonctionnement de la plateforme MentorLink.

## 3\. Analyse préalable

Avant de commencer, il a fallu comprendre :

- les relations entre utilisateurs, profils et publications ;
- la structure des matières fortes et faibles ;
- le fonctionnement des formulaires Django ;
- la récupération dynamique des données depuis la base PostgreSQL.

### Documentation consultée

- Documentation Django Models
- Documentation Django Forms
- Cahier des charges IFRI MentorLink

### Vidéos / tutoriels

- https://youtu.be/M6I--B5k5wo

### Discussions avec l'équipe

- Réunion quotidienne de 18h30
- Discussions techniques avec les membres du groupe

## 4\. Travail effectué

### Étape 1

Analyse des données nécessaires à la publication.

### Étape 2

Création du modèle représentant les offres et demandes.

### Étape 3

Développement du fichier :

publications/models.py

### Étape 4

Création des formulaires dans :

publications/forms.py

### Étape 5

Développement des vues dans :

publications/views.py

### Étape 6

Configuration des routes dans :

publications/urls.py

### Étape 7

Création de la page :

offre.html

permettant la publication des offres.

### Étape 8

Création de la page :

demande.html

permettant la publication des demandes.

### Étape 9

Création de :

offres_correspondantes.html

pour afficher les offres compatibles.

### Étape 10

Création de :

demandes_correspondantes.html

pour afficher les demandes compatibles.

### Étape 11

Connexion des formulaires à la base de données.

### Étape 12

Tests de création et d'enregistrement des publications.

### Étape 13

Validation complète du module.

## 5\. Fichiers créés

| **Fichier** | **Description** |
| --- | --- |
| publications/models.py | Modèle des offres et demandes |
| publications/forms.py | Formulaires |
| publications/views.py | Logique métier |
| publications/urls.py | Routes |
| offre.html | Publication d'offres |
| demande.html | Publication de demandes |
| offres_correspondantes.html | Affichage des offres compatibles |
| demandes_correspondantes.html | Affichage des demandes compatibles |

## 6\. Fichiers modifiés

| **Fichier** | **Nature de la modification** |
| --- | --- |
| publications/models.py | Ajout des modèles |
| publications/forms.py | Création des formulaires |
| publications/views.py | Gestion des publications |
| publications/urls.py | Ajout des routes |

## 7\. Commandes exécutées

python manage.py makemigrations  
<br/>python manage.py migrate  
<br/>python manage.py runserver  
<br/>git add .  
<br/>git commit -m "ajouts des pages de publications d'offres et de demande"  
<br/>git push origin main

## 8\. Difficultés rencontrées

Les matières fortes et faibles n'apparaissaient pas dans les formulaires de publication.

Après plusieurs heures d'investigation, il a été constaté que les utilisateurs présents dans la base avaient été créés avant l'ajout complet des informations de profil.

## 9\. Solution apportée

- Vérification des données stockées.
- Analyse des relations entre modèles.
- Suppression des utilisateurs de test devenus incohérents.
- Recréation des utilisateurs.
- Vérification du chargement des matières.

## 10\. Décisions techniques prises

- Réutilisation directe des compétences du profil.
- Liaison automatique entre utilisateur et publication.
- Séparation des offres et demandes dans l'interface.

## 11\. Livrable obtenu

Système complet de publication d'offres et de demandes fonctionnel.

## 12\. Vérification personnelle

☑ Travail fonctionnel

☑ Architecture respectée

☑ Tests validés

☑ Commit effectué

☑ Push effectué

## 13\. Commit Git associé

**Commit :**

ajouts des pages de publications d'offres et de demande

## 14\. Impact sur le projet

☑ Backend

☑ Base de données

☑ Architecture

## 15\. Travail restant

- Développer le matching.
- Développer la messagerie.

## 16\. Retour personnel

Cette tâche m'a permis de mieux comprendre les relations entre les modèles Django ainsi que l'importance de maintenir des données cohérentes dans la base.

# SECTION N°5

## 1\. Informations générales

**Date :** Nuit du lundi au mardi

**Heure de début :** 20h00

**Heure de fin :** 06h00

**Durée approximative :** 10 heures

**Référence de la tâche :** Développement de l'algorithme de matching mentor-mentoré

**Responsable :** Alexandre

## 2\. Objectif de la tâche

Développer un système permettant de proposer automatiquement des correspondances pertinentes entre mentors et mentorés à partir des compétences et besoins enregistrés.

## 3\. Analyse préalable

Il a fallu comprendre :

- les relations entre profils et publications ;
- les compétences fortes et faibles ;
- les critères de compatibilité.

## 4\. Travail effectué

### Étape 1

Analyse des données disponibles.

### Étape 2

Création de la logique de calcul des correspondances.

### Étape 3

Développement de :

matching/views.py

### Étape 4

Configuration de :

matching/urls.py

### Étape 5

Création de :

matching.html

### Étape 6

Développement du calcul des compatibilités.

### Étape 7

Filtrage des profils compatibles.

### Étape 8

Calcul du score de compatibilité.

### Étape 9

Affichage des résultats.

### Étape 10

Tests du système.

### Étape 11

Correction des erreurs.

### Étape 12

Optimisation de la logique.

### Étape 13

Validation finale.

## 5\. Fichiers créés

| **Fichier** | **Description** |
| --- | --- |
| matching/views.py | Algorithme de matching |
| matching/urls.py | Routes du module |
| matching.html | Affichage des résultats |

## 8\. Difficultés rencontrées

Même problème que pour les publications.

Pendant plusieurs heures, les résultats paraissaient incohérents.

J'ai même été amené à relancer et vérifier plusieurs parties de la base de données avant de comprendre l'origine réelle du problème.

## 9\. Solution apportée

- Analyse approfondie des données.
- Vérification des relations.
- Recréation des données de test.
- Tests successifs jusqu'à obtention des résultats attendus.

## 11\. Livrable obtenu

Algorithme de matching fonctionnel capable de proposer automatiquement des correspondances.

## 13\. Commit Git associé

ajouts de l'algorithme de matching

# SECTION N°6

## 1\. Informations générales

**Date :** Nuit du mardi au mercredi

**Heure de début :** 21h00

**Heure de fin :** 04h00

**Durée approximative :** 7 heures

**Référence de la tâche :** Développement de la messagerie intégrée

**Responsable :** Alexandre

**Collaboration :** Stane

## 2\. Objectif de la tâche

Permettre aux utilisateurs ayant trouvé une correspondance de communiquer directement via la plateforme.

## 4\. Travail effectué

### Étape 1

Analyse du fonctionnement attendu.

### Étape 2

Création du modèle de conversation.

### Étape 3

Création du modèle de message.

### Étape 4

Développement de :

messaging/models.py

### Étape 5

Développement de :

messaging/views.py

### Étape 6

Configuration de :

messaging/urls.py

### Étape 7

Création de :

message.html

### Étape 8

Gestion de l'envoi des messages.

### Étape 9

Gestion de la réception.

### Étape 10

Gestion de l'affichage des conversations.

### Étape 11

Tests entre plusieurs comptes utilisateurs.

### Étape 12

Corrections des anomalies détectées.

### Étape 13

Validation du module.

## 5\. Fichiers créés

| **Fichier** | **Description** |
| --- | --- |
| messaging/models.py | Conversations et messages |
| messaging/views.py | Logique métier |
| messaging/urls.py | Routes |
| message.html | Interface de discussion |

## 8\. Difficultés rencontrées

Complexité de la communication entre utilisateurs et gestion correcte des échanges.

## 9\. Solution apportée

Travail collaboratif avec Stane.

Multiples tests avec différents comptes.

Validation progressive des échanges.

## 11\. Livrable obtenu

Messagerie intégrée fonctionnelle permettant aux utilisateurs d'échanger directement après une mise en relation.

## 13\. Commit Git associé

ajouts de la messagerie intégrée

## 16\. Retour personnel

Cette dernière phase m'a permis de découvrir la gestion des conversations et des interactions entre utilisateurs dans une application web. Le travail réalisé avec Stane a également montré l'importance de la collaboration sur les fonctionnalités les plus complexes du projet.