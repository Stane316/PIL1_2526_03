from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from app.core.models import Utilisateur, Domaine, Besoin, Maitrise
from app.publications.models import Demande, DemandeDomaine, DemandeDisponibilite
from .forms import JOURS_CHOICES, MOMENTS_CHOICES

def formater_publication(pub):
    """
    Helper indispensable pour l'intégration :
    Cette fonction formate un objet 'Demande' de la base de données (unifié dans la table 'publication')
    en un dictionnaire possédant exactement les attributs attendus par vos fichiers HTML unifiés
    (matiere, date_creation, auteur, modalite, etc.).
    """
    # 1. Récupération de la matière (domaine) associée à l'offre/demande
    pub_domaine = DemandeDomaine.objects.filter(demande=pub).first()
    matiere_nom = pub_domaine.domaine.nom if (pub_domaine and pub_domaine.domaine) else "Général"
    
    return {
        'id': pub.id,
        'matiere': matiere_nom,
        'date_creation': pub.date_publication,
        'titre': pub.titre,
        'description': pub.description,
        'auteur': pub.utilisateur,  # pub.utilisateur possède prenom, nom, photo_profil
        'modalite': 'en_ligne' if pub.mode_mentorat == 'EN_LIGNE' else 'presentiel'
    }

def offres_view(request):
    # Sécurité : On récupère l'ID vérifié stocké lors de la connexion
    user_id = request.session.get('verified_user_id')
    
    if not user_id:
        django_messages.error(request, "Veuillez vous connecter pour accéder aux offres.")
        return redirect('connexion')
    
    profil_metier = Utilisateur.objects.filter(id=user_id).first()
    if not profil_metier:
        django_messages.error(request, "Profil utilisateur introuvable. Veuillez vous reconnecter.")
        return redirect('connexion')

    # ON FILTRE UNIQUEMENT les matières maîtrisées par CET utilisateur
    points_forts = Maitrise.objects.filter(utilisateur=profil_metier)
    
    # 1. Récupération des offres de la base de données
    db_mes_offres = Demande.objects.filter(utilisateur=profil_metier, type='OFFRE').order_by('-date_publication')
    db_toutes_les_offres = Demande.objects.filter(type='OFFRE').order_by('-date_publication')

    # 2. Formatage des offres pour correspondre au template HTML unifié
    mes_offres_formatees = [formater_publication(o) for o in db_mes_offres]
    toutes_les_offres_formatees = [formater_publication(o) for o in db_toutes_les_offres]

    if request.method == 'POST':
        ids_choisis = request.POST.getlist('matieres_fortes')
        if ids_choisis:
            nouvelle_offre = Demande.objects.create(
                utilisateur=profil_metier, 
                type='OFFRE', 
                statut='OUVERTE',
                titre="Offre d'aide",
                description=request.POST.get('description', "Je propose mon aide pour accompagner les étudiants sur ces matières."),
                mode_mentorat=request.POST.get('mode_mentorat', 'EN_LIGNE')
            )
            for m_id in ids_choisis:
                domaine_obj = Domaine.objects.filter(id=m_id).first()
                if domaine_obj:
                    DemandeDomaine.objects.create(demande=nouvelle_offre, domaine=domaine_obj)
            return redirect('offres')

    return render(request, 'offres.html', {
        'profil': profil_metier,
        'points_forts': points_forts, # Affiche uniquement ses compétences
        'mes_offres': mes_offres_formatees,
        'offres': toutes_les_offres_formatees,
        'JOURS_CHOICES': JOURS_CHOICES,
    })


def demandes_view(request):
    # Sécurité : On récupère l'ID vérifié stocké lors de la connexion
    user_id = request.session.get('verified_user_id')
    
    if not user_id:
        django_messages.error(request, "Veuillez vous connecter pour accéder aux demandes.")
        return redirect('connexion')
        
    profil_metier = Utilisateur.objects.filter(id=user_id).first()
    if not profil_metier:
        django_messages.error(request, "Profil utilisateur introuvable. Veuillez vous reconnecter.")
        return redirect('connexion')

    # ON FILTRE UNIQUEMENT les besoins (points faibles) de CET utilisateur
    points_faibles = Besoin.objects.filter(utilisateur=profil_metier)
    
    # 1. Récupération des demandes de la base de données
    db_mes_demandes = Demande.objects.filter(utilisateur=profil_metier, type='DEMANDE').order_by('-date_publication')
    db_toutes_les_demandes = Demande.objects.filter(type='DEMANDE').order_by('-date_publication')

    # 2. Formatage des demandes pour correspondre au template HTML unifié
    mes_demandes_formatees = [formater_publication(d) for d in db_mes_demandes]
    toutes_les_demandes_formatees = [formater_publication(d) for d in db_toutes_les_demandes]

    if request.method == 'POST':
        ids_choisis = request.POST.getlist('matieres_faibles')
        if ids_choisis:
            nouvelle_demande = Demande.objects.create(
                utilisateur=profil_metier, 
                type='DEMANDE', 
                statut='OUVERTE',
                titre="Demande d'aide",
                description=request.POST.get('description', "J'ai besoin d'accompagnement sur ces matières pour m'améliorer."),
                mode_mentorat=request.POST.get('mode_mentorat', 'EN_LIGNE')
            )
            for m_id in ids_choisis:
                domaine_obj = Domaine.objects.filter(id=m_id).first()
                if domaine_obj:
                    DemandeDomaine.objects.create(demande=nouvelle_demande, domaine=domaine_obj)
            return redirect('demandes')

    return render(request, 'demandes.html', {
        'profil': profil_metier,
        'points_faibles': points_faibles, # Affiche uniquement ses besoins
        'mes_demandes': mes_demandes_formatees,
        'demandes': toutes_les_demandes_formatees,
        'JOURS_CHOICES': JOURS_CHOICES,
    })