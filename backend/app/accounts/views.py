from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .forms import InscriptionForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from app.core.models import AuthUser
from .forms import ConnexionForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from django.core import signing  # Outil de signature sécurisé de Django
from django.http import HttpResponse

from app.core.models import AuthUser
from .forms import DemandeReinitialisationForm, NouveauMotDePasseForm

from app.core.models import AuthUser
from .forms import DemandeReinitialisationForm, NouveauMotDePasseForm

# Create your views here.
def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # On prépare l'objet en mémoire sans l'enregistrer tout de suite
            utilisateur = form.save(commit=False)
            
            # Étape Cruciale : Hachage sécurisé du mot de passe
            utilisateur.password = make_password(form.cleaned_data['password'])
            
            # Remplissage des valeurs par défaut obligatoires pour la base de données
            utilisateur.is_active = True
            utilisateur.is_staff = False
            utilisateur.is_superuser = False
            utilisateur.date_joined = timezone.now()
            
            # Envoi et insertion propre dans la table 'auth_user' de PostgreSQL
            utilisateur.save()
            
            return redirect('connexion')
    else:
        form = InscriptionForm()
        
    return render(request, 'registration/inscription.html', {'form': form})


def home_page_view(request):
    return render(request ,"home.html")



def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                # On cherche l'utilisateur dans PostgreSQL
                user = AuthUser.objects.get(username=username)
                
                # Étape Cruciale : On vérifie si le mot de passe correspond au hash stocké
                if check_password(password, user.password):
                    if not user.is_active:
                        messages.error(request, "Ce compte est inactif.")
                        return render(request, "registration/login.html", {'form': form})
                    
                    # Authentification réussie ! On stocke les infos clés dans la session
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    
                    # Redirection vers la page de profil ou d'accueil
                    return redirect('profil')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except AuthUser.DoesNotExist:
                messages.error(request, "Nom d'utilisateur introuvable.")
    else:
        form = ConnexionForm()
        
    return render(request, "registration/login.html", {'form': form})

def profil(request):
    return render(request,"profil.html")




from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core import signing  # Outil de signature sécurisé de Django
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from app.core.models import AuthUser
from .forms import DemandeReinitialisationForm, NouveauMotDePasseForm

# 1. Vue pour demander la réinitialisation
def mot_de_passe_oublie_view(request):
    if request.method == 'POST':
        form = DemandeReinitialisationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                # Récupère le premier utilisateur avec cet email
                user = AuthUser.objects.filter(email=email).first()
                
                if user is None:
                    raise AuthUser.DoesNotExist
                
                # Génération d'un token sécurisé contenant le pseudo de l'utilisateur
                token = signing.dumps({'username': user.username})
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Construction du lien
                domaine = request.get_host()
                lien = f"http://{domaine}/reinitialiser-password/{uid}/{token}/"
                
                # Envoi de l'email
                sujet = "Réinitialisation de votre mot de passe - MentorÉtude"
                message_txt = f"Bonjour,\n\nCliquez sur le lien suivant pour réinitialiser votre mot de passe : {lien}\n\nSi vous n'avez pas demandé cette action, l'email peut être ignoré."
                
                send_mail(sujet, message_txt, 'noreply@mentoretude.com', [user.email])
                
                messages.success(request, "Un email contenant un lien de réinitialisation vous a été envoyé.")
                return redirect('connexion')
                
            except AuthUser.DoesNotExist:
                messages.success(request, "Si cet email existe, un lien de réinitialisation vous a été envoyé.")
                return redirect('connexion')
    else:
        form = DemandeReinitialisationForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})


# 2. Vue pour appliquer le nouveau mot de passe
def password_reset_confirm_view(request, uidb64, token):
    try:
        # Décodage de l'UID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = AuthUser.objects.get(pk=uid)
        
        # Vérification du token signé (validité max : 2 heures / 7200 secondes)
        donnees = signing.loads(token, max_age=7200)
        
        # On vérifie que le token appartient bien à cet utilisateur
        if donnees.get('username') != user.username:
            raise signing.BadSignature
            
    except (TypeError, ValueError, OverflowError, AuthUser.DoesNotExist, signing.SignatureExpired, signing.BadSignature):
        user = None

    if user is not None:
        if request.method == 'POST':
            form = NouveauMotDePasseForm(request.POST)
            if form.is_valid():
                # Hachage et sauvegarde dans PostgreSQL
                # On génère le nouveau mot de passe haché
                nouveau_hash = make_password(form.cleaned_data['password']) 

                # On force l'UPDATE direct en base de données SQL
                AuthUser.objects.filter(pk=user.pk).update(password=nouveau_hash)

                messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
                return redirect('connexion')
        else:
            form = NouveauMotDePasseForm()
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse("Le lien de réinitialisation est invalide ou a expiré.", status=400)