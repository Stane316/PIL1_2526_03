import os
import sys
import django
from django.utils import timezone

# 1. Configuration dynamique du chemin pour que Python trouve l'application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 2. Détection et chargement du fichier settings.py
settings_module = None
for root, dirs, files in os.walk(BASE_DIR):
    if 'settings.py' in files:
        folder_name = os.path.basename(root)
        settings_module = f"{folder_name}.settings"
        break

if not settings_module:
    settings_module = 'backend.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
print(f"-> Chargement de la configuration Django via : {settings_module}")
django.setup()

# 3. Imports des modèles (uniquement APRÈS django.setup())
from app.core.models import Utilisateur, Domaine, Besoin, Maitrise
from app.publications.models import Demande, DemandeDomaine

def peupler_donnees():
    print("--- Début du peuplement de la base de données ---")

    # 1. Récupération ou création des matières (Domaines)
    matieres = ['Python', 'SQL', 'Administration Réseau', 'Algèbre', 'Statistiques', 'Recherche Opérationnelle', 'Sécurité Informatique']
    domaines_obj = {}
    for mat in matieres:
        dom, created = Domaine.objects.get_or_create(nom=mat)
        domaines_obj[mat] = dom
    print(f"-> {len(domaines_obj)} matières prêtes.")

    # 2. Profils fictifs adaptés avec numéros de téléphone uniques
    profils_fictifs = [
        {
            'email': 'adelaide.koffi@mentorlink.edu',
            'prenom': 'Adélaïde',
            'nom': 'Koffi',
            'filiere': 'GL',         
            'niveau': 'LICENCE_3',
            'telephone': '+229 91000001', # Téléphone unique ajouté
            'forts': ['Python', 'SQL', 'Statistiques'],
            'faibles': ['Sécurité Informatique']
        },
        {
            'email': 'akim.lawson@mentorlink.edu',
            'prenom': 'Akim',
            'nom': 'Lawson',
            'filiere': 'GL',         
            'niveau': 'LICENCE_3',
            'telephone': '+229 91000002', # Téléphone unique ajouté
            'forts': ['Python', 'SQL', 'Administration Réseau'],
            'faibles': ['Algèbre']
        },
        {
            'email': 'mariam.toure@mentorlink.edu',
            'prenom': 'Mariam',
            'nom': 'Touré',
            'filiere': 'IA',        
            'niveau': 'LICENCE_2',
            'telephone': '+229 91000003', # Téléphone unique ajouté
            'forts': ['Algèbre', 'Statistiques', 'Recherche Opérationnelle'],
            'faibles': ['Python']
        },
        {
            'email': 'christian.bello@mentorlink.edu',
            'prenom': 'Christian',
            'nom': 'Bello',
            'filiere': 'CYBERSECURITE', 
            'niveau': 'LICENCE_3',
            'telephone': '+229 91000004', # Téléphone unique ajouté
            'forts': ['Sécurité Informatique', 'Administration Réseau', 'Python'],
            'faibles': ['Recherche Opérationnelle']
        }
    ]

    for p in profils_fictifs:
        # Recherche ou création par email
        user, created = Utilisateur.objects.get_or_create(
            email=p['email'],
            defaults={
                'prenom': p['prenom'],
                'nom': p['nom'],
                'filiere': p['filiere'],
                'niveau': p['niveau'],
                'telephone': p['telephone'], # Ajouté ici pour les nouveaux inserts
                'actif': True,
                'password_hash': 'fictif_hash_123456',
                'photo_profil': f"https://api.dicebear.com/7.x/avataaars/svg?seed={p['nom']}",
                'created_at': timezone.now()
            }
        )
        
        # Mise à jour si l'utilisateur existait déjà
        if not created:
            user.filiere = p['filiere']
            user.niveau = p['niveau']
            user.prenom = p['prenom']
            user.nom = p['nom']
            user.telephone = p['telephone'] # Ajouté ici pour corriger les anciens profils
            user.save()

        # Nettoyage et insertion des Maîtrises (Points forts)
        Maitrise.objects.filter(utilisateur=user).delete()
        for f in p['forts']:
            Maitrise.objects.create(utilisateur=user, domaine=domaines_obj[f], niveau_maitrise='AVANCE')

        # Nettoyage et insertion des Besoins (Points faibles)
        Besoin.objects.filter(utilisateur=user).delete()
        for fa in p['faibles']:
            Besoin.objects.create(utilisateur=user, domaine=domaines_obj[fa], niveau_priorite=3)

        # Nettoyage et insertion des Demandes / Offres
        Demande.objects.filter(utilisateur=user).delete()

        if p['forts']:
            offre = Demande.objects.create(
                utilisateur=user,
                type='OFFRE',
                statut='OUVERTE',
                titre=f"Aide en {p['forts'][0]}",
                date_publication=timezone.now()
            )
            DemandeDomaine.objects.create(demande=offre, domaine=domaines_obj[p['forts'][0]])

        if p['faibles']:
            demande = Demande.objects.create(
                utilisateur=user,
                type='DEMANDE',
                statut='OUVERTE',
                titre=f"Besoin d'aide en {p['faibles'][0]}",
                date_publication=timezone.now()
            )
            DemandeDomaine.objects.create(demande=demande, domaine=domaines_obj[p['faibles'][0]])

        print(f"-> Utilisateur fictif '{user.prenom} {user.nom}' injecté avec succès.")

    print("--- Fin du peuplement avec succès ! ---")

if __name__ == '__main__':
    peupler_donnees()