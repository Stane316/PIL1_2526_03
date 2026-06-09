from django.shortcuts import render, redirect
from app.core.models import Utilisateur, Domaine, Besoin, Maitrise
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

def matching_view(request):
    """
    Vue principale du matching — Application 'matching'
    """
    # 1. Récupération sécurisée de l'utilisateur connecté pour éviter le crash AuthUser DoesNotExist
    user_id = request.session.get('verified_user_id')
    profil_connecte = None
    
    if user_id:
        profil_connecte = Utilisateur.objects.filter(id=user_id).first()
    
    # Sécurité : Si aucun utilisateur en session, on prend le premier disponible
    if not profil_connecte:
        profil_connecte = Utilisateur.objects.first()

    # Déterminer quel onglet est actif (?tab=offres ou ?tab=demandes)
    onglet_actif = request.GET.get('tab', 'offres')

    # 2. Récupération des matières de l'utilisateur et de la liste complète des domaines
    points_faibles = Besoin.objects.filter(utilisateur=profil_connecte) if profil_connecte else Besoin.objects.none()
    points_forts = Maitrise.objects.filter(utilisateur=profil_connecte) if profil_connecte else Maitrise.objects.none()
    
    # AJOUT ESSENTIEL : On récupère tous les domaines pour alimenter les formulaires de choix
    tous_les_domaines = Domaine.objects.filter(valide=True)

    # Extraction des IDs pour l'algorithme
    mes_besoins_ids = list(points_faibles.values_list('domaine_id', flat=True))
    mes_competences_ids = list(points_forts.values_list('domaine_id', flat=True))

    # Gestion des formulaires de filtrage spécifique (POST)
    if request.method == 'POST':
        if 'submit_demande_specifique' in request.POST:
            ids_choisis = request.POST.getlist('matieres_faibles')
            if ids_choisis:
                mes_besoins_ids = [int(x) for x in ids_choisis]
            onglet_actif = 'offres'
        
        elif 'submit_offre_specifique' in request.POST:
            ids_choisis = request.POST.getlist('matieres_fortes')
            if ids_choisis:
                mes_competences_ids = [int(x) for x in ids_choisis]
            onglet_actif = 'demandes'

    # --- ALGORITHME DE MATCHING ---
    offres_compatibles = []
    demandes_compatibles = []

    if profil_connecte:
        tous_les_utilisateurs = Utilisateur.objects.exclude(id=profil_connecte.id)
        
        for autre_user in tous_les_utilisateurs:
            autre_competences = list(Maitrise.objects.filter(utilisateur=autre_user).values_list('domaine_id', flat=True))
            autre_besoins = list(Besoin.objects.filter(utilisateur=autre_user).values_list('domaine_id', flat=True))

            # --- Onglet Offres (Trouver un Mentor) ---
            if mes_besoins_ids:
                matieres_communes = []
                for b_id in mes_besoins_ids:
                    if b_id in autre_competences:
                        dom = Domaine.objects.filter(id=b_id).first()
                        if dom: matieres_communes.append(dom.nom)

                if matieres_communes:
                    score_matieres = (len(matieres_communes) / len(mes_besoins_ids)) * 60
                    score_filiere = 10 if (profil_connecte.filiere and autre_user.filiere and str(profil_connecte.filiere).upper() == str(autre_user.filiere).upper()) else 0
                    poids_moi = extraire_poids_niveau(profil_connecte.niveau)
                    poids_autre = extraire_poids_niveau(autre_user.niveau)
                    score_niveau = 20 if poids_autre >= poids_moi else 0
                    
                    offres_compatibles.append({
                        'utilisateur': autre_user,
                        'matieres': matieres_communes,
                        'score': int(score_matieres + score_filiere + score_niveau)
                    })

            # --- Onglet Demandes (Aider un Étudiant) ---
            if mes_competences_ids:
                matieres_communes = []
                for c_id in mes_competences_ids:
                    if c_id in autre_besoins:
                        dom = Domaine.objects.filter(id=c_id).first()
                        if dom: matieres_communes.append(dom.nom)

                if matieres_communes:
                    score_matieres = (len(matieres_communes) / len(mes_competences_ids)) * 60
                    score_filiere = 10 if (profil_connecte.filiere and autre_user.filiere and str(profil_connecte.filiere).upper() == str(autre_user.filiere).upper()) else 0
                    poids_moi = extraire_poids_niveau(profil_connecte.niveau)
                    poids_autre = extraire_poids_niveau(autre_user.niveau)
                    score_niveau = 20 if poids_moi >= poids_autre else 0
                    
                    demandes_compatibles.append({
                        'utilisateur': autre_user,
                        'matieres': matieres_communes,
                        'score': int(score_matieres + score_filiere + score_niveau)
                    })

        # Tri par score décroissant
        offres_compatibles = sorted(offres_compatibles, key=lambda x: x['score'], reverse=True)
        demandes_compatibles = sorted(demandes_compatibles, key=lambda x: x['score'], reverse=True)

    # Renvoi du contexte complet au template matching.html
    # CORRECTION : Filtrage pour n'afficher que les matières du profil connecté selon l'onglet actif
    if onglet_actif == 'offres':
        domaines_a_afficher = [pf.domaine for pf in points_faibles]
    else:
        domaines_a_afficher = [pf.domaine for pf in points_forts]

    # AJOUT SÉCURITÉ : On récupère la liste de tous les domaines valides pour remplir le formulaire de gauche
    domaines_formulaire = Domaine.objects.filter(valide=True)

    return render(request, 'matching.html', {
        'profil': profil_connecte,
        'points_faibles': points_faibles,
        'points_forts': points_forts,
        'tous_les_domaines': domaines_formulaire,  # On utilise domaines_formulaire pour afficher les matières à cocher
        'offres_compatibles': offres_compatibles,
        'demandes_compatibles': demandes_compatibles,
        'onglet_actif': onglet_actif,
        'jours_choices': JOURS_CHOICES,
        'moments_choices': MOMENTS_CHOICES
    })