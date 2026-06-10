from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from app.core.models import Utilisateur
from app.messaging.models import Conversation, Message

def message_view(request, conversation_id=None):
    # Sécurité session
    user_id = request.session.get('verified_user_id')
    if not user_id: 
        return redirect('connexion')
        
    profil_connecte = Utilisateur.objects.filter(id=user_id).first()

    # 1. Récupérer toutes les conversations de l'utilisateur (soit il est créateur, soit destinataire)
    discussions = Conversation.objects.filter(Q(createur=profil_connecte) | Q(destinataire=profil_connecte))

    conversation_active = None
    messages = []

    # 2. Si une conversation spécifique est sélectionnée
    if conversation_id:
        conversation_active = get_object_or_404(Conversation, id=conversation_id)
        # Sécurité : s'assurer que l'utilisateur fait partie de la conversation
        if conversation_active.createur != profil_connecte and conversation_active.destinataire != profil_connecte:
            return redirect('message')
        
        # Envoi d'un nouveau message
        # Dans ton views.py, à l'intérieur du bloc 'if request.method == 'POST':'
        if request.method == 'POST':
            contenu = request.POST.get('contenu', '').strip()
            if contenu:
                Message.objects.create(
                    conversation=conversation_active,
                    expediteur=profil_connecte,
                    contenu=contenu
                )
                # Important : rediriger après l'enregistrement pour éviter les doublons
                return redirect('message_chat', conversation_id=conversation_id)

        messages = conversation_active.messages.all()

    # Formater les discussions pour identifier facilement l'interlocuteur dans le template
    liste_chats = []
    for disc in discussions:
        interlocuteur = disc.destinataire if disc.createur == profil_connecte else disc.createur
        liste_chats.append({
            'obj': disc,
            'interlocuteur': interlocuteur
        })

    return render(request, 'message.html', {
        'titre_page': 'Messages',
        'profil': profil_connecte,
        'liste_chats': liste_chats,
        'conversation_active': conversation_active,
        'messages': messages,
        'interlocuteur_actif': conversation_active.destinataire if conversation_active and conversation_active.createur == profil_connecte else (conversation_active.createur if conversation_active else None)
    })

from django.db import connection  # NE PAS OUBLIER CET IMPORT TOUT EN HAUT SI CE N'EST PAS FAIT

def démarrer_discussion_view(request, autre_user_id):
    """ Action déclenchée par le bouton 'Contacter' """
    user_id = request.session.get('verified_user_id')
    if not user_id: 
        return redirect('connexion')
        
    moi = Utilisateur.objects.get(id=user_id)
    l_autre = get_object_or_404(Utilisateur, id=autre_user_id)

    # 1. Vérifier si une conversation existe déjà
    discussion = Conversation.objects.filter(
        (Q(createur=moi) & Q(destinataire=l_autre)) | 
        (Q(createur=l_autre) & Q(destinataire=moi))
    ).first()

    # 2. Sinon, on la crée proprement (l'ID va remonter nickel grâce au setval)
    if not discussion:
        discussion = Conversation.objects.create(createur=moi, destinataire=l_autre)

    # 3. Redirection vers le chat actif
    return redirect('message_chat', conversation_id=discussion.id)