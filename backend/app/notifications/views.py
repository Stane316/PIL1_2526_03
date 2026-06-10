from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from app.core.models import Utilisateur
from app.notifications.models import Notification

def notifications_view(request):
    # 1. Sécurité : Vérification de l'utilisateur connecté
    user_id = request.session.get('verified_user_id')
    if not user_id:
        django_messages.error(request, "Veuillez vous connecter pour accéder à vos notifications.")
        return redirect('connexion')
        
    user_email = request.session.get('verified_user_email')
    profil_metier = Utilisateur.objects.filter(email=user_email).first()
    
    if not profil_metier:
        django_messages.error(request, "Profil utilisateur introuvable.")
        return redirect('connexion')

    # 2. GESTION DU POST : Tout marquer comme lu
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'tout_marquer_lu':
            # Met à jour le champ 'lu' à True pour toutes les notifications de l'utilisateur
            Notification.objects.filter(utilisateur=profil_metier, lu=False).update(lu=True)
            return redirect('notifications')

    # 3. RÉCUPÉRATION DES NOTIFICATIONS DE L'UTILISATEUR
    # On ordonne du plus récent au plus ancien
    db_notifications = Notification.objects.filter(utilisateur=profil_metier).order_by('-created_at')
    
    # 4. CARTOGRAPHIE DES SOUCIS D'ATTRIBUTS AVEC LE TEMPLATE
    # Notre SQL utilise (type_notification, lu, created_at)
    # Votre template HTML attend (type, lue, date_creation)
    # Nous adaptons les dictionnaires à la volée de manière ultra-élégante :
    liste_notifications = []
    for notif in db_notifications:
        liste_notifications.append({
            'id': notif.id,
            'type': notif.type_notification,  # 'match', 'message', 'offre', 'demande', etc.
            'contenu': notif.contenu,
            'lue': notif.lu,                   # lu -> lue
            'date_creation': notif.created_at  # created_at -> date_creation
        })
    
    return render(request, 'notifications.html', {
        'titre_page': 'Notifications',
        'profil': profil_metier,
        'notifications': liste_notifications
    })