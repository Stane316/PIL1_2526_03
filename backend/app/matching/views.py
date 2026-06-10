from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from app.core.models import Utilisateur, Domaine, Besoin, Maitrise, DisponibiliteUtilisateur
from app.publications.models import Demande, DemandeDomaine, DemandeDisponibilite
from app.publications.forms import JOURS_CHOICES, MOMENTS_CHOICES

def extraire_poids_niveau(niveau_str):
    """Transforme les enums réels de la base de données en score numérique pour comparaison"""
    if not niveau_str:
        return 0
    niveau = niveau_str.upper().strip()
    mapping = {
        'LICENCE_1': 1,
        'LICENCE_2': 2,
        'LICENCE_3': 3,
        'MASTER_1': 4,
        'MASTER_2': 5
    }
    return mapping.get(niveau, 0)

def verifier_dispos_compatibles(dispos_moi, dispos_autre):
    """
    Calcule s'il y a un chevauchement temporel entre deux listes de disponibilités d'utilisateurs.
    """
    for d_moi in dispos_moi:
        for d_autre in dispos_autre:
            if d_moi.jour_semaine == d_autre.jour_semaine:
                # Deux créneaux se chevauchent si : max(debut_a, debut_b) < min(fin_a, fin_b)
                max_debut = max(d_moi.heure_debut, d_autre.heure_debut)
                min_fin = min(d_moi.heure_fin, d_autre.heure_fin)
                if max_debut < min_fin:
                    return True
    return False

def matching_view(request):
    """
    Vue principale du matching — Application 'matching'
    Calcule un score précis sur 100 points :
    - 60 % Compatibilité matières (Sujets communs)
    - 20 % Compatibilité disponibilités (Chevauchements de créneaux généraux)
    - 10 % Compatibilité filière (Même département d'études)
    - 10 % Compatibilité niveau (Niveau d'étude académique cohérent)
    """
    # 1. Sécurité : Vérification de la connexion
    user_id = request.session.get('verified_user_id')
    if not user_id:
        django_messages.error(request, "Veuillez vous connecter pour accéder au matching.")
        return redirect('connexion')
        
    profil_connecte = Utilisateur.objects.filter(id=user_id).first()
    if not profil_connecte:
        django_messages.error(request, "Profil utilisateur introuvable. Veuillez vous reconnecter.")
        return redirect('connexion')

    # Déterminer quel onglet est actif (?tab=offres ou ?tab=demandes)
    onglet_actif = request.GET.get('tab', 'offres')

    # 2. Récupération des compétences (matières fortes) et besoins (matières faibles) du connecté
    points_faibles = Besoin.objects.filter(utilisateur=profil_connecte)
    points_forts = Maitrise.objects.filter(utilisateur=profil_connecte)
    
    # Récupération des disponibilités générales de l'utilisateur connecté
    dispos_moi = DisponibiliteUtilisateur.objects.filter(utilisateur=profil_connecte)

    # Extraction des IDs pour l'algorithme
    mes_besoins_ids = list(points_faibles.values_list('domaine_id', flat=True))
    mes_competences_ids = list(points_forts.values_list('domaine_id', flat=True))

    # --- ALGORITHME DE MATCHING ---
    offres_compatibles = []
    demandes_compatibles = []

    tous_les_utilisateurs = Utilisateur.objects.exclude(id=profil_connecte.id)
    
    for autre_user in tous_les_utilisateurs:
        # Récupération des forces, faiblesses et dispos de l'autre utilisateur
        autre_competences = list(Maitrise.objects.filter(utilisateur=autre_user).values_list('domaine_id', flat=True))
        autre_besoins = list(Besoin.objects.filter(utilisateur=autre_user).values_list('domaine_id', flat=True))
        dispos_autre = DisponibiliteUtilisateur.objects.filter(utilisateur=autre_user)

        # 1. Calcul de la compatibilité des disponibilités (Poids : 20 points)
        a_un_chevauchement = verifier_dispos_compatibles(dispos_moi, dispos_autre)
        score_dispo = 20 if a_un_chevauchement else 0

        # 2. Calcul de la filière (Poids : 10 points)
        score_filiere = 10 if (profil_connecte.filiere and autre_user.filiere and str(profil_connecte.filiere).upper() == str(autre_user.filiere).upper()) else 0

        # Poids académiques pour le niveau (Poids : 10 points)
        poids_moi = extraire_poids_niveau(profil_connecte.niveau)
        poids_autre = extraire_poids_niveau(autre_user.niveau)

        # ════════════════════════════════════════════════════════════
        # ONGLET OFFRES : Trouver un Mentor (L'autre utilisateur propose ce dont j'ai besoin)
        # ════════════════════════════════════════════════════════════
        if mes_besoins_ids:
            matieres_communes = []
            for b_id in mes_besoins_ids:
                if b_id in autre_competences:
                    dom = Domaine.objects.filter(id=b_id).first()
                    if dom: matieres_communes.append(dom.nom)

            # On n'affiche le profil que s'il y a au moins une compétence commune
            if matieres_communes:
                # 60% basé sur le ratio de besoins couverts
                score_matieres = (len(matieres_communes) / len(mes_besoins_ids)) * 60
                
                # Le mentor doit avoir un niveau supérieur ou égal pour enseigner (10%)
                score_niveau = 10 if poids_autre >= poids_moi else 0
                
                score_total = int(score_matieres + score_dispo + score_filiere + score_niveau)
                
                offres_compatibles.append({
                    'utilisateur': autre_user,
                    'matieres': matieres_communes,
                    'score': score_total
                })

        # ════════════════════════════════════════════════════════════
        # ONGLET DEMANDES : Aider un Étudiant (L'autre utilisateur a besoin de ce que je maîtrise)
        # ════════════════════════════════════════════════════════════
        if mes_competences_ids:
            matieres_communes = []
            for c_id in mes_competences_ids:
                if c_id in autre_besoins:
                    dom = Domaine.objects.filter(id=c_id).first()
                    if dom: matieres_communes.append(dom.nom)

            # On n'affiche le profil que s'il y a au moins un besoin commun
            if matieres_communes:
                # 60% basé sur le ratio de compétences proposées
                score_matieres = (len(matieres_communes) / len(mes_competences_ids)) * 60
                
                # L'étudiant aidé doit idéalement être d'un niveau inférieur ou égal (10%)
                score_niveau = 10 if poids_moi >= poids_autre else 0
                
                score_total = int(score_matieres + score_dispo + score_filiere + score_niveau)
                
                demandes_compatibles.append({
                    'utilisateur': autre_user,
                    'matieres': matieres_communes,
                    'score': score_total
                })

    # Tri par score décroissant (les plus compatibles d'abord)
    offres_compatibles = sorted(offres_compatibles, key=lambda x: x['score'], reverse=True)
    demandes_compatibles = sorted(demandes_compatibles, key=lambda x: x['score'], reverse=True)

    # Récupération des matières à afficher sur le profil connecté
    if onglet_actif == 'offres':
        domaines_a_afficher = [pf.domaine for pf in points_faibles]
    else:
        domaines_a_afficher = [pf.domaine for pf in points_forts]

    # Récupération des domaines validés pour le formulaire de filtrage
    tous_les_domaines = Domaine.objects.filter(valide=True)

    return render(request, 'matching.html', {
        'profil': profil_connecte,
        'points_faibles': points_faibles,
        'points_forts': points_forts,
        'tous_les_domaines': tous_les_domaines,
        'offres_compatibles': offres_compatibles,
        'demandes_compatibles': demandes_compatibles,
        'onglet_actif': onglet_actif,
        'jours_choices': JOURS_CHOICES,
        'moments_choices': MOMENTS_CHOICES
    })