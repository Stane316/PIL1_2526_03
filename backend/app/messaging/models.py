from django.db import models
from app.core.models import Utilisateur
from app.mentorat.models import RelationMentorat

class Conversation(models.Model):
    relation = models.OneToOneField(RelationMentorat, on_delete=models.CASCADE, db_column='relation_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'conversation'
        managed = True


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', db_column='conversation_id')
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='expediteur_id')
    contenu = models.TextField(db_column='contenu')
    lu = models.BooleanField(default=False, db_column='lu')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'message'
        managed = True