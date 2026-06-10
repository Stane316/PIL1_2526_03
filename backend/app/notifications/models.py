from django.db import models
from app.core.models import Utilisateur

class Notification(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='utilisateur_id')
    type_notification = models.CharField(max_length=50, db_column='type_notification') # MESSAGE, REPONSE, SYSTEME
    contenu = models.TextField(db_column='contenu')
    lu = models.BooleanField(default=False, db_column='lu')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'notification'
        managed = True