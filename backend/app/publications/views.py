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
    
    # 2. Récupération d'une disponibilité textuelle formatée pour l'affichage
    pub_dispo = DemandeDisponibilite.objects.filter(demande=pub).first()
    dispo_libelle = "Disponibilité non précisée"
    if pub_dispo:
        jours_map = {1: 'Lundi', 2: 'Mardi', 3: 'Mercredi', 4: 'Jeudi', 5: 'Vendredi', 6: 'Samedi', 7: 'Dimanche'}
        jour_nom = jours_map.get(pub_dispo.jour_semaine, 'Samedi')
        moments_map = {'08:00:00': 'matin', '14:00:00': 'après-midi', '18:00:00': 'soir'}
        moment_nom = moments_map.get(str(pub_dispo.heure_debut), 'matin')
        dispo_libelle = f"{jour_nom} {moment_nom}"
        
    return {
        'id': pub.id,
        'matiere': matiere_nom,
        'date_creation': pub.date_publication,
        'titre': pub.titre,
        'description': pub.description,
        'auteur': pub.utilisateur,  # pub.utilisateur possède prenom, nom, photo_profil
        'modalite': 'en_ligne' if pub.mode_mentorat == 'EN_LIGNE' else 'presentiel',
        'disponibilite': dispo_libelle
    }

def enregistrer_disponibilite_texte(demande_obj, dispo_texte):
    """
    Helper intelligent d'analyse :
    Analyse le texte saisi de façon libre par l'étudiant (ex: 'Lundi soir' ou 'Samedi matin')
    et l'enregistre sous forme d'une ligne structurée et requêtable dans DemandeDisponibilite.
    """
    if not dispo_texte:
        return
        
    text = dispo_texte.lower().strip()
    
    # Détermination du jour de la semaine
    jour = 6  # Samedi par défaut
    if 'lun' in text: jour = 1
    elif 'mar' in text: jour = 2
    elif 'mer' in text: jour = 3
    elif 'jeu' in text: jour = 4
    elif 'ven' in text: jour = 5
    elif 'sam' in text: jour = 6
    elif 'dim' in text: jour = 7
    
    # Détermination du créneau horaire
    h_debut = '08:00:00'
    h_fin = '12:00:00'
    if 'soir' in text or 'nuit' in text:
        h_debut = '18:00:00'
        h_fin = '21:00:00'
    elif 'aprem' in text or 'midi' in text or 'après' in text:
        h_debut = '14:00:00'
        h_fin = '18:00:00'
        
    # Création de l'enregistrement de disponibilité
    DemandeDisponibilite.objects.create(
        demande=demande_obj,
        jour_semaine=jour,
        heure_debut=h_debut,
        heure_fin=h_fin
    )

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
    
    # 1. Traitement de la création d'offre (Saisie POST par l'utilisateur)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        matiere_nom = request.POST.get('matiere')
        description = request.POST.get('description')
        modalite = request.POST.get('modalite', 'en_ligne')
        dispo_texte = request.POST.get('disponibilite')
        
        # En base de données, la modalité (mode_mentorat) reçoit 'EN_LIGNE' ou 'PRESENTIEL'
        mode_mentorat = 'EN_LIGNE' if modalite == 'en_ligne' else 'PRESENTIEL'
        
        if titre and matiere_nom:
            # Création de l'offre
            nouvelle_offre = Demande.objects.create(
                utilisateur=profil_metier, 
                type='OFFRE', 
                statut='OUVERTE',
                titre=titre,
                description=description,
                mode_mentorat=mode_mentorat
            )
            # Recherche de la matière (Domaine) par son nom
            domaine_obj = Domaine.objects.filter(nom=matiere_nom).first()
            if domaine_obj:
                DemandeDomaine.objects.create(demande=nouvelle_offre, domaine=domaine_obj)
            
            # Analyse intelligente et sauvegarde de la disponibilité spécifiée
            if dispo_texte:
                enregistrer_disponibilite_texte(nouvelle_offre, dispo_texte)
                
            django_messages.success(request, "Votre offre d'aide a été publiée avec succès !")
            return redirect('offres')

    # 2. Récupération des offres de la base de données
    db_mes_offres = Demande.objects.filter(utilisateur=profil_metier, type='OFFRE').order_by('-date_publication')
    db_toutes_les_offres = Demande.objects.filter(type='OFFRE').order_by('-date_publication')

    # 3. Formatage des offres pour correspondre au template HTML unifié
    mes_offres_formatees = [formater_publication(o) for o in db_mes_offres]
    toutes_les_offres_formatees = [formater_publication(o) for o in db_toutes_les_offres]

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
    
    # 1. Traitement de la création de demande (Saisie POST par l'utilisateur)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        matiere_nom = request.POST.get('matiere')
        description = request.POST.get('description')
        dispo_texte = request.POST.get('disponibilite')
        
        if titre and matiere_nom:
            # Création de la demande
            nouvelle_demande = Demande.objects.create(
                utilisateur=profil_metier, 
                type='DEMANDE', 
                statut='OUVERTE',
                titre=titre,
                description=description,
                mode_mentorat='EN_LIGNE'
            )
            # Recherche de la matière (Domaine) par son nom
            domaine_obj = Domaine.objects.filter(nom=matiere_nom).first()
            if domaine_obj:
                DemandeDomaine.objects.create(demande=nouvelle_demande, domaine=domaine_obj)
            
            # Analyse intelligente et sauvegarde de la disponibilité spécifiée
            if dispo_texte:
                enregistrer_disponibilite_texte(nouvelle_demande, dispo_texte)
                
            django_messages.success(request, "Votre demande d'aide a été publiée avec succès !")
            return redirect('demandes')

    # 2. Récupération des demandes de la base de données
    db_mes_demandes = Demande.objects.filter(utilisateur=profil_metier, type='DEMANDE').order_by('-date_publication')
    db_toutes_les_demandes = Demande.objects.filter(type='DEMANDE').order_by('-date_publication')

    # 3. Formatage des demandes pour correspondre au template HTML unifié
    mes_demandes_formatees = [formater_publication(d) for d in db_mes_demandes]
    toutes_les_demandes_formatees = [formater_publication(d) for d in db_toutes_les_demandes]

    return render(request, 'demandes.html', {
        'profil': profil_metier,
        'points_faibles': points_faibles, # Affiche uniquement ses besoins
        'mes_demandes': mes_demandes_formatees,
        'demandes': toutes_les_demandes_formatees,
        'JOURS_CHOICES': JOURS_CHOICES,
    })