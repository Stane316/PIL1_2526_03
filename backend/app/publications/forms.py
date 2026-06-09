from django import forms
from app.core.models import Domaine, Besoin

JOURS_CHOICES = [
    ('LUNDI', 'Lundi'), ('MARDI', 'Mardi'), ('MERCREDI', 'Mercredi'),
    ('JEUDI', 'Jeudi'), ('VENDREDI', 'Vendredi'), ('SAMEDI', 'Samedi'), ('DIMANCHE', 'Dimanche')
]

MOMENTS_CHOICES = [
    ('MATIN', 'Matin (7h-11h)'),
    ('MIDI', 'Midi (11h-13h)'),
    ('APRES-MIDI', 'Après-midi (13h-19h)'),
    ('SOIR', 'Soir (19h-23h)')
]

class FormulaireDemande(forms.Form):
    # On laisse le queryset vide par défaut, il sera rempli dans la vue
    matieres = forms.ModelMultipleChoiceField(
        queryset=Domaine.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Dans quelles matières avez-vous des lacunes ?"
    )