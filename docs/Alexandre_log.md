## **IFRI MentorLink - Member Work Log (Alexandre)** 

## Rôle principal : Développeur Backend Django 

Organisation : Réunion quotidienne à 18h30 pour synchronisation, répartition des tâches et résolution des blocages. 

## **SECTION 2 - Création et modification du profil utilisateur** 

## Fichiers modifiés : 

- profil/views.py : logique de création, consultation et modification du profil. 

- profil/urls.py : routes liées au profil utilisateur. 

- profil.html : affichage des informations du profil. 

- frontend/registration/modif.html : formulaire de modification des informations utilisateur. 

## Travail réalisé : 

- Gestion des informations personnelles. 

- Ajout de la photo de profil. 

- Gestion des matières maîtrisées (points forts). 

- Gestion des matières à améliorer (points faibles). 

- Mise à jour des données utilisateur. 

- Validation et sauvegarde des informations dans la base de données. 

## Commit Git : 

- 'depot contenant la creation complete du profil utilisateur' 

## **SECTION 3 - Création des pages HTML et navigation** 

## Fichiers créés/modifiés : 

- navbar.html : barre de navigation globale. 

- header.html : en-tête commun du site. 

- Pages HTML secondaires nécessaires à la navigation générale. 

- Configuration des routes permettant l'accès aux différentes interfaces. 

## Travail réalisé : 

- Création de l'interface utilisateur générale. 

- Uniformisation de la navigation. 

- Intégration des liens entre les différentes pages. 

- Préparation du frontend pour les fonctionnalités backend. 

- Amélioration de l'expérience utilisateur. 

## Commit Git : 

'Depot des pages html' 

## **SECTION 4 - Offres, demandes de mentorat et fonctionnalités métier** 

## Fichiers modifiés : 

- publications/views.py : gestion des offres et demandes. 

- publications/urls.py : routes des publications. 

- publications/models.py : modèles de données des offres et demandes. 

- publications/forms.py : formulaires de création. 

- demande.html : création et consultation des demandes. 

- offre.html : création et consultation des offres. 

- demandes_correspondantes.html : affichage des demandes compatibles. 

- offres_correspondantes.html : affichage des offres compatibles. 

- matching/views.py : logique de matching. 

- matching/urls.py : routes du matching. 

- matching.html : affichage des résultats de compatibilité. 

- messaging/views.py : gestion de la messagerie. 

- messaging/models.py : stockage des conversations et messages. 

- messaging/urls.py : routes de la messagerie. 

- message.html : interface de discussion. 

## Travail réalisé : 

- Création des offres de mentorat. 

- Création des demandes de mentorat. 

- Liaison avec les compétences du profil utilisateur. 

- Affichage des correspondances. 

- Mise en place de l'algorithme de matching. 

- Création de la messagerie intégrée permettant aux utilisateurs d'échanger. 

## Difficulté rencontrée : 

Les matières fortes et faibles n'apparaissaient pas dans les formulaires car les utilisateurs avaient été créés avant la mise en place complète des profils. 

## Solution : 

Réinitialisation des données concernées, recréation des utilisateurs et vérification des relations entre les modèles. 

## Commits Git : 

- 'ajouts des pages de publications d'offres et de demande' 

- 'ajouts de l'algorithme de matching' 

- 'ajouts de la messagerie intégrée' 

