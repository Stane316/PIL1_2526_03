from django.shortcuts import render, redirect
from app.core.models import Utilisateur, Domaine, Besoin, Maitrise
from app.publications.models import Demande, DemandeDomaine, DemandeDisponibilite
from .forms import JOURS_CHOICES, MOMENTS_CHOICES

def offres_view(request):
    # On récupère l'ID vérifié stocké lors de la connexion
    user_id = request.session.get('verified_user_id')
    
    # Stratégie de récupération du profil métier (Utilisateur)
    profil_metier = Utilisateur.objects.filter(id=user_id).first() or Utilisateur.objects.first()

    # ON FILTRE UNIQUEMENT les matières maîtrisées par CET utilisateur
    points_forts = Maitrise.objects.filter(utilisateur=profil_metier)
    
    # Historique personnel et global
    mes_offres = Demande.objects.filter(utilisateur=profil_metier, type='OFFRE').order_by('-date_publication')
    toutes_les_offres = Demande.objects.filter(type='OFFRE').order_by('-date_publication')

    if request.method == 'POST':
        ids_choisis = request.POST.getlist('matieres_fortes')
        if ids_choisis:
            nouvelle_offre = Demande.objects.create(
                utilisateur=profil_metier, 
                type='OFFRE', 
                statut='OUVERTE',
                titre="Offre d'aide"
            )
            for m_id in ids_choisis:
                domaine_obj = Domaine.objects.filter(id=m_id).first()
                if domaine_obj:
                    DemandeDomaine.objects.create(demande=nouvelle_offre, domaine=domaine_obj)
            return redirect('offres')

    return render(request, 'offres.html', {
        'profil': profil_metier,
        'points_forts': points_forts, # Affiche uniquement ses compétences
        'mes_offres': mes_offres,
        'offres': toutes_les_offres,
        'JOURS_CHOICES': JOURS_CHOICES,
    })


def demandes_view(request):
    user_id = request.session.get('verified_user_id')
    profil_metier = Utilisateur.objects.filter(id=user_id).first() or Utilisateur.objects.first()

    # ON FILTRE UNIQUEMENT les besoins (points faibles) de CET utilisateur
    points_faibles = Besoin.objects.filter(utilisateur=profil_metier)
    
    # Historique personnel et global
    mes_demandes = Demande.objects.filter(utilisateur=profil_metier, type='DEMANDE').order_by('-date_publication')
    toutes_les_demandes = Demande.objects.filter(type='DEMANDE').order_by('-date_publication')

    if request.method == 'POST':
        ids_choisis = request.POST.getlist('matieres_faibles')
        if ids_choisis:
            nouvelle_demande = Demande.objects.create(
                utilisateur=profil_metier, 
                type='DEMANDE', 
                statut='OUVERTE',
                titre="Demande d'aide"
            )
            for m_id in ids_choisis:
                domaine_obj = Domaine.objects.filter(id=m_id).first()
                if domaine_obj:
                    DemandeDomaine.objects.create(demande=nouvelle_demande, domaine=domaine_obj)
            return redirect('demandes')

    return render(request, 'demandes.html', {
        'profil': profil_metier,
        'points_faibles': points_faibles, # Affiche uniquement ses besoins
        'mes_demandes': mes_demandes,
        'demandes': toutes_les_demandes,
        'JOURS_CHOICES': JOURS_CHOICES,
    })