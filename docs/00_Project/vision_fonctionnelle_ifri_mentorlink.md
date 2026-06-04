# Vision Fonctionnelle IFRI MentorLink v1

## 1\. Présentation du projet

IFRI MentorLink est une plateforme web de mentorat académique destinée aux étudiants de l'IFRI.

L'objectif de la plateforme est de faciliter la mise en relation entre des étudiants possédant des compétences dans certains domaines et d'autres étudiants ayant besoin d'aide dans ces mêmes domaines.

La plateforme vise à structurer l'entraide académique au sein de l'IFRI en permettant aux étudiants de trouver rapidement les personnes les plus aptes à les accompagner selon leurs besoins.

# 2\. Problématique

Au sein de l'IFRI, de nombreux étudiants rencontrent des difficultés dans certaines matières ou compétences.

Parallèlement, d'autres étudiants maîtrisent ces domaines et pourraient les aider.

Actuellement, ces mises en relation se font principalement de manière informelle :

- par bouche-à-oreille ;
- dans les groupes WhatsApp ;
- à travers les réseaux sociaux ;
- ou via les connaissances personnelles.

Ce fonctionnement présente plusieurs limites :

- difficulté à identifier les personnes compétentes ;
- absence de système de recommandation ;
- manque de suivi ;
- perte de temps dans la recherche d'aide.

IFRI MentorLink vise à résoudre ce problème grâce à un système de mise en relation intelligent.

# 3\. Objectifs du système

Les objectifs principaux sont :

- permettre aux étudiants de présenter leurs compétences ;
- permettre aux étudiants d'exprimer leurs besoins d'apprentissage ;
- faciliter la publication d'offres et de demandes de mentorat ;
- proposer automatiquement des correspondances pertinentes ;
- permettre aux utilisateurs d'échanger via une messagerie intégrée ;
- favoriser l'entraide et le partage de connaissances au sein de l'IFRI.

# 4\. Acteurs du système

Le système ne distingue pas les utilisateurs dès leur inscription.

Chaque utilisateur est simplement un étudiant de l'IFRI.

Selon le contexte, un même utilisateur peut être :

- mentor ;
- mentoré ;
- ou les deux simultanément.

Exemple :

Jean peut être mentor en Python et mentoré en Cybersécurité.

# 5\. Concepts fondamentaux

## Compétence / Domaine

Une compétence représente un domaine de connaissance ou une matière.

Exemples :

- Python ;
- SQL ;
- Réseaux ;
- Cybersécurité ;
- Intelligence Artificielle ;
- Machine Learning ;
- Développement Web.

Dans le système, la distinction entre matière et compétence n'est pas nécessaire.

Toutes sont considérées comme des domaines de connaissance.

## Compétence maîtrisée

Une compétence maîtrisée représente un domaine dans lequel l'utilisateur estime pouvoir aider d'autres étudiants.

Chaque compétence possède un niveau :

- Débutant ;
- Intermédiaire ;
- Avancé.

## Lacune

Une lacune représente un domaine dans lequel l'utilisateur souhaite progresser.

Chaque lacune possède également un niveau indiquant l'importance du besoin.

## Disponibilité

Une disponibilité représente une plage horaire pendant laquelle l'utilisateur peut participer à une activité de mentorat.

Chaque disponibilité contient :

- un jour ;
- une heure de début ;
- une heure de fin.

Exemple :

Lundi - 18h00 à 20h00.

# 6\. Publication de mentorat

Le système repose sur deux types de publications.

## Offre de mentorat

Une offre est publiée par un étudiant souhaitant aider d'autres étudiants.

Exemple :

"Je peux accompagner des étudiants en Python et SQL."

## Demande de mentorat

Une demande est publiée par un étudiant recherchant de l'aide.

Exemple :

"Je cherche de l'aide en Linux."

# 7\. Réponses aux publications

Une publication peut recevoir plusieurs réponses.

Exemple :

Une demande de mentorat peut recevoir plusieurs propositions provenant de différents mentors.

Le créateur de la publication reste libre de choisir la personne qui lui semble la plus adaptée.

Le système doit lui présenter les informations nécessaires pour prendre sa décision :

- score de compatibilité ;
- domaines concernés ;
- disponibilités communes ;
- informations de profil.

# 8\. Système de matching

Le système de matching constitue le cœur fonctionnel de la plateforme.

Son objectif est d'identifier automatiquement les utilisateurs les plus compatibles.

Le calcul du score repose principalement sur :

## Compatibilité des domaines

Le système compare :

- les compétences maîtrisées du mentor ;
- les lacunes du mentoré.

Plus le nombre de domaines correspondants est élevé, plus le score est important.

## Compatibilité des disponibilités

Le système recherche les créneaux horaires communs.

Plus le nombre de créneaux compatibles est élevé, plus le score augmente.

## Compatibilité académique

Le système prend également en compte :

- la filière ;
- le niveau d'étude.

Ces critères ont un poids inférieur aux compétences et aux disponibilités mais permettent d'améliorer la pertinence des recommandations.

# 9\. Relation mentor-mentoré

Une relation mentor-mentoré n'est pas permanente.

Elle existe pour répondre à un besoin précis.

Exemple :

Jean aide Paul en Python.

Lorsque Paul estime avoir atteint son objectif d'apprentissage, la relation peut être clôturée.

Une même paire d'utilisateurs peut avoir plusieurs relations successives concernant différents domaines.

# 10\. Multiplicité des relations

Le système autorise :

## Plusieurs mentorés pour un mentor

Exemple :

Jean accompagne :

- Paul en Python ;
- Alice en SQL ;
- Sarah en Git.

## Plusieurs mentors pour un mentoré

Exemple :

Paul apprend :

- Python avec Jean ;
- SQL avec Alice ;
- Linux avec Sarah.

# 11\. Messagerie

Lorsqu'une relation est acceptée, une conversation privée est automatiquement créée.

Les utilisateurs peuvent :

- envoyer des messages ;
- recevoir des messages ;
- consulter l'historique de leurs échanges.

La première version du projet prend uniquement en charge les messages textuels.

L'ajout futur de pièces jointes, images et documents est prévu dans les évolutions possibles du système.

# 12\. Sécurité

Le système doit garantir :

- l'unicité des comptes ;
- la confidentialité des données ;
- la protection des informations personnelles ;
- le stockage sécurisé des mots de passe.

Les mots de passe doivent être stockés sous forme hashée.

# 13\. Vision d'évolution

L'application doit être conçue de manière évolutive afin de permettre l'ajout futur de fonctionnalités telles que :

- système de réputation ;
- notation des mentors ;
- validation des compétences ;
- pièces jointes dans les conversations ;
- visioconférence ;
- statistiques de mentorat ;
- tableau de bord avancé ;
- recommandations intelligentes améliorées.

# 14\. Résumé

IFRI MentorLink est une plateforme de mentorat académique intelligente permettant aux étudiants de l'IFRI :

- d'exprimer leurs besoins ;
- de valoriser leurs compétences ;
- de trouver rapidement les personnes les plus adaptées ;
- d'échanger facilement ;
- de développer une communauté d'entraide durable.

Le cœur du système repose sur trois piliers :

- Gestion des profils et compétences.
- Matching intelligent mentor-mentoré.
- Communication via une messagerie intégrée.