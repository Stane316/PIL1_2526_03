from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from django.http import JsonResponse
from app.core.models import Utilisateur
from app.messaging.models import Conversation, Message
from app.mentorat.models import RelationMentorat, Reponse

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

    # 2. AUTOMATION : Création automatique d'une conversation si ?contact=ID est fourni dans l'URL
    contact_id = request.GET.get('contact')
    if contact_id:
        contact_user = Utilisateur.objects.filter(id=contact_id).first()
        if contact_user and contact_user != profil:
            relation = RelationMentorat.objects.filter(
                mentor=profil, mentore=contact_user
            ).first() or RelationMentorat.objects.filter(
                mentor=contact_user, mentore=profil
            ).first()
            
            if not relation:
                # Recherche ou création d'une publication pour respecter la contrainte NOT NULL de reponse.publication_id
                from app.publications.models import Demande
                pub = Demande.objects.filter(utilisateur=contact_user).first()
                if not pub:
                    pub = Demande.objects.create(
                        utilisateur=contact_user,
                        type='OFFRE',
                        statut='OUVERTE',
                        titre="Discussion directe",
                        description="Discussion directe initiée depuis le matching",
                        mode_mentorat='EN_LIGNE'
                    )
                
                reponse_liaison = Reponse.objects.create(
                    publication=pub,
                    auteur=profil,
                    message="Liaison automatique initiée depuis le profil",
                    statut='ACCEPTEE'
                )
                
                relation = RelationMentorat.objects.create(
                    mentor=contact_user,
                    mentore=profil,
                    reponse=reponse_liaison,
                    statut='ACTIVE'
                )
                
            conversation = Conversation.objects.filter(relation=relation).first()
            if not conversation:
                conversation = Conversation.objects.create(relation=relation)
                
            return redirect(f"/messages/?conv={conversation.id}")

    # 3. GESTION DU POST : Envoi d'un message
    if request.method == 'POST':
        conv_id = request.POST.get('conv_id')
        contenu = request.POST.get('contenu')
        
        if conv_id and contenu:
            conversation = Conversation.objects.filter(id=conv_id).first()
            if conversation and (conversation.relation.mentor == profil or conversation.relation.mentore == profil):
                Message.objects.create(
                    conversation=conversation,
                    expediteur=profil,
                    contenu=contenu,
                    lu=False
                )
                return redirect(f"/messages/?conv={conv_id}")

    # 4. RÉCUPÉRATION DE TOUTES LES CONVERSATIONS DE L'UTILISATEUR (MENTOR OU MENTORÉ)
    db_conversations = Conversation.objects.filter(
        relation__mentor=profil
    ) | Conversation.objects.filter(
        relation__mentore=profil
    )
    
    liste_conversations = []
    for conv in db_conversations:
        if conv.relation.mentor == profil:
            interlocuteur = conv.relation.mentore
        else:
            interlocuteur = conv.relation.mentor
            
        dernier_msg = conv.messages.order_by('-created_at').first()
        dernier_msg_data = None
        if dernier_msg:
            dernier_msg_data = {
                'contenu': dernier_msg.contenu,
                'date': dernier_msg.created_at,
            }
            
        nb_non_lus = conv.messages.filter(expediteur=interlocuteur, lu=False).count()
        interlocuteur.en_ligne = True
        
        liste_conversations.append({
            'id': conv.id,
            'interlocuteur': interlocuteur,
            'dernier_message': dernier_msg_data,
            'nb_non_lus': nb_non_lus
        })

    # 5. GESTION DE LA CONVERSATION ACTIVE (SÉLECTIONNÉE)
    conversation_active = None
    messages_conv = []
    
    active_conv_id = request.GET.get('conv')
    if active_conv_id:
        conv_active_obj = Conversation.objects.filter(id=active_conv_id).first()
        
        if conv_active_obj and (conv_active_obj.relation.mentor == profil or conv_active_obj.relation.mentore == profil):
            if conv_active_obj.relation.mentor == profil:
                interlocuteur_active = conv_active_obj.relation.mentore
            else:
                interlocuteur_active = conv_active_obj.relation.mentor
                
            conv_active_obj.messages.filter(expediteur=interlocuteur_active, lu=False).update(lu=True)
            
            conversation_active = {
                'id': conv_active_obj.id,
                'interlocuteur': interlocuteur_active
            }
            
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
        'messages_conv': messages_conv,
        'sans_footer': True,  # Supprime le footer parasite de la page de chat !
    }
    
    return render(request, 'message.html', context)


# ============================================================
# API ENDPOINTS POUR LE CHAT ASYNCHRONE EN DIRECT (REAL-TIME LOOK)
# ============================================================

def message_api_view(request, conv_id):
    """
    Retourne la liste complète des messages d'une conversation sous format JSON.
    Marque automatiquement les messages reçus comme 'lus'.
    """
    user_id = request.session.get('verified_user_id')
    if not user_id:
        return JsonResponse({'error': 'Non connecté'}, status=401)
        
    profil = Utilisateur.objects.filter(id=user_id).first()
    conv = Conversation.objects.filter(id=conv_id).first()
    
    if not conv or (conv.relation.mentor != profil and conv.relation.mentore != profil):
        return JsonResponse({'error': 'Accès interdit'}, status=403)
        
    # Déterminer l'interlocuteur pour marquer les messages reçus comme 'lus'
    if conv.relation.mentor == profil:
        interlocuteur = conv.relation.mentore
    else:
        interlocuteur = conv.relation.mentor
        
    # Marquage des messages entrants comme lus
    conv.messages.filter(expediteur=interlocuteur, lu=False).update(lu=True)
    
    # Extraction des messages
    db_messages = conv.messages.order_by('created_at')
    messages_list = []
    for m in db_messages:
        messages_list.append({
            'id': m.id,
            'expediteur_id': m.expediteur.id,
            'expediteur_nom': f"{m.expediteur.prenom} {m.expediteur.nom}",
            'contenu': m.contenu,
            'date': m.created_at.strftime('%H:%M'),
            'lu': m.lu
        })
        
    return JsonResponse({
        'messages': messages_list,
        'profil_id': profil.id
    })


def envoyer_message_api(request, conv_id):
    """
    Enregistre un nouveau message envoyé de manière asynchrone (AJAX via fetch)
    et renvoie le message créé au format JSON.
    """
    user_id = request.session.get('verified_user_id')
    if not user_id:
        return JsonResponse({'error': 'Non connecté'}, status=401)
        
    profil = Utilisateur.objects.filter(id=user_id).first()
    conv = Conversation.objects.filter(id=conv_id).first()
    
    if not conv or (conv.relation.mentor != profil and conv.relation.mentore != profil):
        return JsonResponse({'error': 'Accès interdit'}, status=403)
        
    if request.method == 'POST':
        import json
        try:
            # Saisie JSON (fetch api)
            data = json.loads(request.body)
            contenu = data.get('contenu')
        except:
            # Saisie Form classique
            contenu = request.POST.get('contenu')
            
        if contenu:
            msg = Message.objects.create(
                conversation=conv,
                expediteur=profil,
                contenu=contenu,
                lu=False
            )
            return JsonResponse({
                'success': True,
                'message': {
                    'id': msg.id,
                    'expediteur_id': msg.expediteur.id,
                    'expediteur_nom': f"{msg.expediteur.prenom} {msg.expediteur.nom}",
                    'contenu': msg.contenu,
                    'date': msg.created_at.strftime('%H:%M'),
                    'lu': msg.lu
                }
            })
            
    return JsonResponse({'error': 'Requête invalide'}, status=400)
