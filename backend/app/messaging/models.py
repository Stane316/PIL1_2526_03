from django.db import models
from app.core.models import Utilisateur

class Conversation(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')  
    createur = models.ForeignKey(Utilisateur, models.CASCADE, db_column='createur_id', related_name='conversations_creees')
    destinataire = models.ForeignKey(Utilisateur, models.CASCADE, db_column='destinataire_id', related_name='conversations_recues')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'conversation'

class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, models.CASCADE, db_column='conversation_id', related_name='messages')
    expediteur = models.ForeignKey(Utilisateur, models.CASCADE, db_column='expediteur_id')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'message'
        ordering = ['date_envoi']