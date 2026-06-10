from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from django.http import JsonResponse
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
            Notification.objects.filter(utilisateur=profil_metier, lu=False).update(lu=True)
            return redirect('notifications')

    # 3. RÉCUPÉRATION DES NOTIFICATIONS DE L'UTILISATEUR
    db_notifications = Notification.objects.filter(utilisateur=profil_metier).order_by('-created_at')
    
    liste_notifications = []
    for notif in db_notifications:
        liste_notifications.append({
            'id': notif.id,
            'type': notif.type_notification,
            'contenu': notif.contenu,
            'lue': notif.lu,
            'date_creation': notif.created_at
        })
    
    return render(request, 'notifications.html', {
        'titre_page': 'Notifications',
        'profil': profil_metier,
        'notifications': liste_notifications
    })


# ============================================================
# API ENDPOINT POUR LES NOTIFICATIONS ASYNCHRONES EN DIRECT (REAL-TIME)
# ============================================================

def notifications_api_view(request):
    """
    Retourne la liste des notifications non lues ou de toutes les notifications en JSON.
    Permet un rafraîchissement asynchrone régulier pour un effet "temps réel" conforme.
    """
    user_id = request.session.get('verified_user_id')
    if not user_id:
        return JsonResponse({'error': 'Non connecté'}, status=401)
        
    profil = Utilisateur.objects.filter(id=user_id).first()
    if not profil:
        return JsonResponse({'error': 'Profil introuvable'}, status=404)
        
    db_notifications = Notification.objects.filter(utilisateur=profil).order_by('-created_at')
    liste_notifications = []
    
    for notif in db_notifications:
        # Convert timesince in python style or let JS handle it, standard date formatting is easier
        liste_notifications.append({
            'id': notif.id,
            'type': notif.type_notification,
            'contenu': notif.contenu,
            'lue': notif.lu,
            'date': notif.created_at.strftime('%d %b à %H:%M')
        })
        
    return JsonResponse({
        'notifications': liste_notifications,
        'nb_non_lus': Notification.objects.filter(utilisateur=profil, lu=False).count()
    })
