from django.db import models
from app.core.models import Utilisateur, Domaine 

class Demande(models.Model):
    # 'auteur_id' correspond à la colonne de ta table 'publication'
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, db_column='auteur_id')
    date_publication = models.DateTimeField(auto_now_add=True, db_column='created_at')
    type = models.CharField(max_length=20, default='DEMANDE', db_column='type_publication')
    statut = models.CharField(max_length=20, default='OUVERTE', db_column='statut')
    titre = models.CharField(max_length=255, default='Demande d\'aide')
    description = models.TextField(default='')
    mode_mentorat = models.CharField(max_length=20, default='EN_LIGNE', db_column='mode_mentorat')
    
    class Meta:
        db_table = 'publication'  # Utilise ta vraie table SQL d'origine
        managed = True      # Activé pour permettre la migration automatique sur une base vide !

class DemandeDomaine(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, db_column='publication_id')
    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE, db_column='domaine_id')

    class Meta:
        db_table = 'publication_domaine'  # Utilise ta vraie table SQL d'origine
        managed = True      # Activé !

class DemandeDisponibilite(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, db_column='publication_id')
    # Ton script initial utilise SMALLINT (1 à 7) pour les jours et TIME pour les heures
    jour_semaine = models.IntegerField(db_column='jour_semaine')     
    heure_debut = models.TimeField(db_column='heure_debut', default='08:00:00') 
    heure_fin = models.TimeField(db_column='heure_fin', default='18:00:00') 

    class Meta:
        db_table = 'disponibilite_publication'  # Utilise ta vraie table SQL d'origine
        managed = True      