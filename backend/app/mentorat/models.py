from django.db import models
from app.core.models import Utilisateur, Domaine
from app.publications.models import Demande

class Reponse(models.Model):
    publication = models.ForeignKey(Demande, on_delete=models.CASCADE, db_column='publication_id')
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='auteur_id')
    message = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, default='EN_ATTENTE')  # EN_ATTENTE, ACCEPTEE, REFUSEE
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reponse'
        managed = True  # Permet à Django de synchroniser ce modèle avec le SQL


class ReponseDomaine(models.Model):
    reponse = models.ForeignKey(Reponse, on_delete=models.CASCADE, db_column='reponse_id')
    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE, db_column='domaine_id')

    class Meta:
        db_table = 'reponse_domaine'
        unique_together = (('reponse', 'domaine'),)
        managed = True


class RelationMentorat(models.Model):
    mentor = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='mentor_relations', db_column='mentor_id')
    mentore = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='mentore_relations', db_column='mentore_id')
    reponse = models.OneToOneField(Reponse, on_delete=models.CASCADE, db_column='reponse_id')
    statut = models.CharField(max_length=20, default='ACTIVE')  # ACTIVE, TERMINEE, ANNULEE
    date_debut = models.DateTimeField(auto_now_add=True, db_column='date_debut')
    date_fin = models.DateTimeField(blank=True, null=True, db_column='date_fin')
    commentaire_fin = models.TextField(blank=True, null=True, db_column='commentaire_fin')

    class Meta:
        db_table = 'relation_mentorat'
        managed = True


class RelationDomaine(models.Model):
    relation = models.ForeignKey(RelationMentorat, on_delete=models.CASCADE, db_column='relation_id')
    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE, db_column='domaine_id')

    class Meta:
        db_table = 'relation_domaine'
        unique_together = (('relation', 'domaine'),)
        managed = True