from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from app.core.models import Utilisateur
from app.messaging.models import Conversation, Message
from app.mentorat.models import RelationMentorat

def message_view(request):
    # 1. Vérification de la connexion
    user_id = request.session.get('verified_user_id')
    if not user_id:
        django_messages.error(request, "Veuillez vous connecter pour accéder à votre messagerie.")
        return redirect('connexion')
        
    user_email = request.session.get('verified_user_email')
    profil = Utilisateur.objects.filter(email=user_email).first()
    if not profil:
        django_messages.error(request, "Profil utilisateur introuvable.")
        return redirect('connexion')

    # 2. GESTION DU POST : Envoi d'un message
    if request.method == 'POST':
        conv_id = request.POST.get('conv_id')
        contenu = request.POST.get('contenu')
        
        if conv_id and contenu:
            # On vérifie que la conversation existe et que l'utilisateur y participe
            conversation = Conversation.objects.filter(id=conv_id).first()
            if conversation and (conversation.relation.mentor == profil or conversation.relation.mentore == profil):
                # Création et sauvegarde du message
                Message.objects.create(
                    conversation=conversation,
                    expediteur=profil,
                    contenu=contenu,
                    lu=False
                )
                # Redirection vers la même page avec le paramètre de conversation active
                return redirect(f"/messages/?conv={conv_id}")

    # 3. RÉCUPÉRATION DE TOUTES LES CONVERSATIONS DE L'UTILISATEUR (MENTOR OU MENTORÉ)
    # On filtre les conversations via la relation de mentorat associée
    db_conversations = Conversation.objects.filter(
        relation__mentor=profil
    ) | Conversation.objects.filter(
        relation__mentore=profil
    )
    
    # On structure les conversations pour le template HTML
    liste_conversations = []
    for conv in db_conversations:
        # L'interlocuteur est l'autre personne de la relation
        if conv.relation.mentor == profil:
            interlocuteur = conv.relation.mentore
        else:
            interlocuteur = conv.relation.mentor
            
        # Récupération du dernier message
        dernier_msg = conv.messages.order_by('-created_at').first()
        
        # Adaptation des propriétés attendues par votre template (date, contenu, lu)
        dernier_msg_data = None
        if dernier_msg:
            dernier_msg_data = {
                'contenu': dernier_msg.contenu,
                'date': dernier_msg.created_at,
            }
            
        # Nombre de messages non lus pour cet interlocuteur
        nb_non_lus = conv.messages.filter(expediteur=interlocuteur, lu=False).count()
        
        # Un attribut factice "en_ligne" (votre template l'attend, on le met par défaut à True pour la démo)
        interlocuteur.en_ligne = True  # Vous pouvez lier cela à un statut de session plus tard
        
        liste_conversations.append({
            'id': conv.id,
            'interlocuteur': interlocuteur,
            'dernier_message': dernier_msg_data,
            'nb_non_lus': nb_non_lus
        })

    # 4. GESTION DE LA CONVERSATION ACTIVE (SÉLECTIONNÉE)
    conversation_active = None
    messages_conv = []
    
    active_conv_id = request.GET.get('conv')
    if active_conv_id:
        # On recherche la conversation demandée
        conv_active_obj = Conversation.objects.filter(id=active_conv_id).first()
        
        # Sécurité : On s'assure que l'utilisateur connecté fait bien partie de cette conversation
        if conv_active_obj and (conv_active_obj.relation.mentor == profil or conv_active_obj.relation.mentore == profil):
            
            # Définir l'interlocuteur de la conversation active
            if conv_active_obj.relation.mentor == profil:
                interlocuteur_active = conv_active_obj.relation.mentore
            else:
                interlocuteur_active = conv_active_obj.relation.mentor
                
            # Marquer tous les messages reçus dans cette conversation comme lus
            conv_active_obj.messages.filter(expediteur=interlocuteur_active, lu=False).update(lu=True)
            
            conversation_active = {
                'id': conv_active_obj.id,
                'interlocuteur': interlocuteur_active
            }
            
            # Récupérer l'historique des messages pour l'affichage (ordonné du plus ancien au plus récent)
            db_messages = conv_active_obj.messages.order_by('created_at')
            for msg in db_messages:
                messages_conv.append({
                    'expediteur': msg.expediteur,
                    'contenu': msg.contenu,
                    'date': msg.created_at,
                    'lu': msg.lu
                })

    context = {
        'titre_page': 'Messagerie',
        'profil': profil,
        'conversations': liste_conversations,
        'conversation_active': conversation_active,
        'messages_conv': messages_conv
    }
    
    return render(request, 'message.html', context)