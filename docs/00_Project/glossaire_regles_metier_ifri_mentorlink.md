# Glossaire et Règles Métier IFRI MentorLink v1

## 1\. Objectif du document

Ce document définit les termes métier utilisés dans IFRI MentorLink ainsi que les règles de fonctionnement du système.

Son objectif est de garantir une compréhension commune entre tous les membres de l’équipe de développement avant le début de la conception technique.

# 2\. Glossaire

## Utilisateur

Étudiant inscrit sur la plateforme IFRI MentorLink.

Un utilisateur peut être :

- mentor ;
- mentoré ;
- ou les deux simultanément.

L’utilisateur constitue l’entité centrale du système.

## Mentor

Utilisateur possédant des compétences dans un ou plusieurs domaines et souhaitant accompagner d’autres étudiants.

Un mentor n’est pas un rôle permanent.

Un utilisateur peut être mentor dans un domaine et mentoré dans un autre.

## Mentoré

Utilisateur ayant besoin d’aide dans un ou plusieurs domaines.

Le statut de mentoré dépend du besoin exprimé et n’est pas permanent.

## Domaine

Représente une matière, une compétence ou un sujet de connaissance.

Exemples :

- Python
- SQL
- Linux
- Réseaux
- Cybersécurité
- Intelligence Artificielle

Le système ne distingue pas les matières des compétences.

Toutes sont considérées comme des domaines de connaissance.

## Compétence

Association entre un utilisateur et un domaine qu’il maîtrise.

Une compétence possède un niveau :

- Débutant
- Intermédiaire
- Avancé

## Lacune

Association entre un utilisateur et un domaine dans lequel il souhaite progresser.

Une lacune possède un niveau indiquant l’intensité du besoin.

## Disponibilité

Créneau horaire pendant lequel un utilisateur peut participer à une activité de mentorat.

Une disponibilité contient :

- Jour
- Heure de début
- Heure de fin

## Offre de mentorat

Publication créée par un utilisateur souhaitant accompagner d’autres étudiants.

L’offre précise :

- les domaines concernés ;
- les disponibilités ;
- le mode d’accompagnement.

## Demande de mentorat

Publication créée par un utilisateur recherchant de l’aide.

La demande précise :

- les domaines concernés ;
- les disponibilités ;
- le mode souhaité.

## Réponse

Manifestation d’intérêt envoyée à une offre ou une demande.

Une réponse permet à deux utilisateurs d’entrer dans un processus de mise en relation.

## Matching

Processus automatique permettant de calculer un score de compatibilité entre deux utilisateurs.

## Relation de mentorat

Lien actif entre un mentor et un mentoré pour un domaine donné.

La relation possède un cycle de vie.

## Conversation

Canal de communication privé créé automatiquement lorsqu’une relation de mentorat est acceptée.

# 3\. Règles métier générales

## RM-001

Chaque utilisateur doit posséder un compte unique.

## RM-002

Une adresse email ne peut être utilisée qu’une seule fois.

## RM-003

Un numéro de téléphone ne peut être utilisé qu’une seule fois.

## RM-004

Les mots de passe doivent être stockés sous forme hashée.

## RM-005

Chaque utilisateur peut modifier son profil à tout moment.

# 4\. Règles liées aux compétences

## RM-006

Un utilisateur peut posséder plusieurs compétences.

## RM-007

Un utilisateur peut posséder plusieurs lacunes.

## RM-008

Un domaine peut être associé à plusieurs utilisateurs.

## RM-009

Une compétence possède obligatoirement un niveau.

## RM-010

Une lacune possède obligatoirement un niveau.

# 5\. Règles liées aux disponibilités

## RM-011

Un utilisateur peut définir plusieurs disponibilités.

## RM-012

Chaque disponibilité possède :

- un jour ;
- une heure de début ;
- une heure de fin.

## RM-013

L’heure de fin doit être supérieure à l’heure de début.

## RM-014

Deux disponibilités identiques ne doivent pas être enregistrées plusieurs fois pour le même utilisateur.

# 6\. Règles liées aux publications

## RM-015

Un utilisateur peut publier plusieurs offres de mentorat.

## RM-016

Un utilisateur peut publier plusieurs demandes de mentorat.

## RM-017

Une publication possède un état :

- ACTIVE
- PAUSED
- CLOSED

## RM-018

Une publication peut être modifiée par son auteur.

## RM-019

Une publication peut être fermée puis réactivée.

# 7\. Règles liées aux réponses

## RM-020

Une publication peut recevoir plusieurs réponses.

## RM-021

Un utilisateur peut répondre à plusieurs publications.

## RM-022

Le créateur d’une publication peut accepter ou refuser une réponse.

## RM-023

L’acceptation d’une réponse peut entraîner la création d’une relation de mentorat.

# 8\. Règles liées au matching

## RM-024

Le matching doit prendre en compte les domaines communs.

## RM-025

Le matching doit prendre en compte les disponibilités communes.

## RM-026

Le matching doit prendre en compte la filière.

## RM-027

Le matching doit prendre en compte le niveau académique.

## RM-028

Le score de compatibilité est compris entre 0 et 100.

## RM-029

Le score doit être présenté à l’utilisateur.

# 9\. Règles liées aux relations de mentorat

## RM-030

Une relation de mentorat concerne un domaine précis.

## RM-031

Un mentor peut accompagner plusieurs mentorés.

## RM-032

Un mentoré peut avoir plusieurs mentors.

## RM-033

Une relation possède un état :

- ACTIVE
- PAUSED
- COMPLETED
- CANCELLED

## RM-034

Une relation peut être clôturée lorsque l’objectif pédagogique est atteint.

## RM-035

Une relation clôturée reste conservée dans l’historique.

# 10\. Règles liées à la messagerie

## RM-036

Une conversation est créée automatiquement lors de la création d’une relation de mentorat.

## RM-037

Une conversation appartient à une seule relation de mentorat.

## RM-038

Les messages textuels sont conservés dans l’historique.

## RM-039

Les utilisateurs doivent pouvoir consulter leurs anciennes conversations.

## RM-040

Les notifications de nouveaux messages doivent être envoyées en temps réel.

# 11\. Règles liées à la sécurité

## RM-041

Un utilisateur ne peut accéder qu’à ses propres données privées.

## RM-042

Les actions sensibles nécessitent une authentification.

## RM-043

Les données personnelles doivent être protégées.

# 12\. Règles d’évolution du système

## RM-044

L’architecture doit permettre l’ajout futur de nouvelles fonctionnalités.

## RM-045

Le système doit permettre l’ajout futur d’un système de réputation.

## RM-046

Le système doit permettre l’ajout futur de pièces jointes dans les conversations.

## RM-047

Le système doit permettre l’ajout futur de mécanismes avancés de validation des compétences.

# 13\. Principes de conception retenus

1.  Simplicité d’utilisation.
2.  Extensibilité.
3.  Sécurité.
4.  Maintenabilité.
5.  Documentation systématique.
6.  Collaboration via Git.
7.  Respect du cahier des charges.