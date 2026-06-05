from django import forms
from app.core.models import AuthUser

class InscriptionForm(forms.ModelForm):
    # Champ mot de passe configuré pour masquer la saisie (●●●●)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-100 rounded-lg p-3 outline-none focus:ring-2 focus:ring-indigo-500',
        'placeholder': 'Mot de passe'
    }))

    class Meta:
        model = AuthUser
        # On extrait uniquement les 5 champs nécessaires pour un formulaire d'inscription
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        
        # Stylisation Tailwind de tes inputs pour qu'ils reprennent ton design d'origine
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'bg-gray-100 rounded-lg p-3 outline-none focus:ring-2 focus:ring-indigo-500', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-gray-100 rounded-lg p-3 outline-none focus:ring-2 focus:ring-indigo-500', 'placeholder': 'Nom'}),
            'username': forms.TextInput(attrs={'class': 'bg-gray-100 rounded-lg p-3 outline-none focus:ring-2 focus:ring-indigo-500', 'placeholder': "Nom d'utilisateur"}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-100 rounded-lg p-3 outline-none focus:ring-2 focus:ring-indigo-500', 'placeholder': 'Email'}),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # On vérifie si le username existe déjà dans la table auth_user
        if AuthUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # On vérifie si l'email existe déjà dans la table auth_user
        if AuthUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée pour un autre compte.")
        return email


class ConnexionForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-100 border-none rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 outline-none',
            'placeholder': "Nom d'utilisateur"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-gray-100 border-none rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 outline-none',
            'placeholder': '••••••••'
        })
    )

# partie changer de mot de passe

class DemandeReinitialisationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-gray-100 border-none rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 outline-none',
            'placeholder': 'exemple@email.com'
        })
    )

class NouveauMotDePasseForm(forms.Form):
    password = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-gray-100 border-none rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 outline-none',
            'placeholder': '••••••••'
        })
    )
    confirm_password = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-gray-100 border-none rounded-lg p-3 focus:ring-2 focus:ring-indigo-500 outline-none',
            'placeholder': '••••••••'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas.")
        return cleaned_data