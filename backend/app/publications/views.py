from django.shortcuts import render, redirect
from app.core.models import Utilisateur, Domaine, Besoin, Maitrise
from app.publications.models import Demande, DemandeDomaine, DemandeDisponibilite
from .forms import JOURS_CHOICES, MOMENTS_CHOICES

def offres_view(request):
    user_id = request.session.get('verified_user_id')
    profil_metier = Utilisateur.objects.filter(id=user_id).first() or Utilisateur.objects.first()

    points_forts = Maitrise.objects.filter(utilisateur=profil_metier)
    mes_offres = Demande.objects.filter(utilisateur=profil_metier, type='OFFRE').order_by('-date_publication')

    if request.method == 'POST':
        ids_choisis = request.POST.getlist('matieres_fortes')
        if ids_choisis:
            nouvelle_offre = Demande.objects.create(
                utilisateur=profil_metier, 
                type='OFFRE', 
                statut='OUVERTE',
                titre='Offre d\'aide'
            )
            for m_id in ids_choisis:
                domaine_obj = Domaine.objects.filter(id=m_id).first()
                if domaine_obj:
                    DemandeDomaine.objects.create(demande=nouvelle_offre, domaine=domaine_obj)
            
            mapping_jours = {'LUNDI': 1, 'MARDI': 2, 'MERCREDI': 3, 'JEUDI': 4, 'VENDREDI': 5, 'SAMEDI': 6, 'DIMANCHE': 7}
            for key, value in request.POST.items():
                if key.startswith('dispo_') and value == '1':
                    parts = key.split('_')
                    DemandeDisponibilite.objects.create(
                        demande=nouvelle_offre,
                        jour_semaine=mapping_jours.get(parts[1], 0),
                        heure_debut='08:00:00',
                        heure_fin='18:00:00'
                    )
            return redirect('offres')

    # CORRECTION ICI : 'profil': profil_metier au lieu de laisser l'ancien format
    return render(request, 'offres.html', {
        'profil': profil_metier,
        'points_forts': points_forts,
        'mes_offres': mes_offres,
        'jours_choices': JOURS_CHOICES,
        'moments_choices': MOMENTS_CHOICES
    })

def demandes_view(request):
    user_id = request.session.get('verified_user_id')
    profil_metier = Utilisateur.objects.filter(id=user_id).first() or Utilisateur.objects.first()

    points_faibles = Besoin.objects.filter(utilisateur=profil_metier)
    mes_demandes = Demande.objects.filter(utilisateur=profil_metier, type='DEMANDE').order_by('-date_publication')

    if request.method == 'POST':
        ids_choisis = request.POST.getlist('matieres_faibles')
        if ids_choisis:
            nouvelle_demande = Demande.objects.create(utilisateur=profil_metier, type='DEMANDE', statut='OUVERTE')
            
            for m_id in ids_choisis:
                domaine_obj = Domaine.objects.filter(id=m_id).first()
                if domaine_obj:
                    DemandeDomaine.objects.create(demande=nouvelle_demande, domaine=domaine_obj)
            
            mapping_jours = {'LUNDI': 1, 'MARDI': 2, 'MERCREDI': 3, 'JEUDI': 4, 'VENDREDI': 5, 'SAMEDI': 6, 'DIMANCHE': 7}
            for key, value in request.POST.items():
                if key.startswith('dispo_') and value == '1':
                    parts = key.split('_')
                    DemandeDisponibilite.objects.create(
                        demande=nouvelle_demande,
                        jour_semaine=mapping_jours.get(parts[1], 0),
                        heure_debut='08:00:00',
                        heure_fin='18:00:00'
                    )
            return redirect('demandes')

    # CORRECTION ICI : Ajout de 'profil': profil_metier pour le header
    return render(request, 'demandes.html', {
        'profil': profil_metier,
        'points_faibles': points_faibles,
        'mes_demandes': mes_demandes,
        'jours_choices': JOURS_CHOICES,
        'moments_choices': MOMENTS_CHOICES
    })