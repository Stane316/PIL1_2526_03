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


from app.core.models import AuthUser, Utilisateur, Domaine, Maitrise, Besoin

from django.core import signing  # Outil de signature sécurisé de Django
from django.http import HttpResponse

from app.core.models import AuthUser
from .forms import DemandeReinitialisationForm, NouveauMotDePasseForm

from app.core.models import AuthUser
from .forms import DemandeReinitialisationForm, NouveauMotDePasseForm

from django.core import signing
from django.contrib.auth.hashers import make_password
from app.core.models import AuthUser
from .forms import InscriptionForm

from django.utils import timezone
from datetime import timedelta
from app.core.models import AuthUser


import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Create your views here.

def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # 1. Hachage du mot de passe
            user.password = make_password(form.cleaned_data['password'])
            
            # 2. Remplir les contraintes NOT NULL de PostgreSQL pour l'utilisateur standard
            user.is_superuser = False
            user.is_staff = False
            user.date_joined = timezone.now()  # Optionnel mais recommandé si la colonne existe
            
            # 3. Le compte est désactivé en attendant la confirmation par email
            user.is_active = False
            
            # 4. Sauvegarde finale dans PostgreSQL
            user.save()
            
            # 5. Génération du token d'activation
            token = signing.dumps({'username': user.username})
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construction du lien d'activation
            domaine = request.get_host()
            lien_activation = f"http://{domaine}/activer-compte/{uid}/{token}/"
            
            # Envoi de l'email
            sujet = "Activez votre compte - MentorÉtude"
            message_txt = f"Bonjour {user.first_name},\n\nMerci pour votre inscription ! Activez votre compte via ce lien : {lien_activation}"
            
            send_mail(sujet, message_txt, 'noreply@mentoretude.com', [user.email])
            
            messages.success(request, "Inscription réussie ! Un email de confirmation vous a été envoyé.")
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'registration/inscription.html', {'form': form})

def home_page_view(request):
    return render(request ,"home.html")



from django.contrib.auth import login  # <-- AJOUTER CET IMPORT TOUT EN HAUT

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = AuthUser.objects.get(username=username)
                
                if check_password(password, user.password):
                    if not user.is_active:
                        messages.error(request, "Votre compte n'est pas encore activé. Vérifiez vos emails.")
                        return render(request, "registration/login.html", {'form': form})
                    
                    # On stocke les variables clés dans la session pour la vue profil
                    request.session['verified_user_id'] = user.id
                    request.session['verified_user_email'] = user.email
                    request.session['username'] = user.username
                    
                    return redirect('profil')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except AuthUser.DoesNotExist:
                messages.error(request, "Nom d'utilisateur introuvable.")
    else:
        form = ConnexionForm()
        
    return render(request, "registration/login.html", {'form': form})

#def profil(request):
    #return render(request,"profil.html")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.core.models import Utilisateur, Maitrise, Besoin

# On force l'utilisateur à être connecté pour voir son profil
#@login_required(login_url='connexion')
def profil(request):
    # Sécurité : On vérifie si l'ID utilisateur est bien présent dans la session
    user_email = request.session.get('verified_user_email')
    user_id = request.session.get('verified_user_id')
    
    if not user_email:
        messages.error(request, "Veuillez vous connecter pour accéder à votre profil.")
        return redirect('connexion')

    try:
        # 1. On récupère le compte d'authentification pour avoir le nom/prénom de base
        user_auth = AuthUser.objects.get(id=user_id)
        
        # 2. On récupère le profil métier dans la table 'utilisateur' via l'email
        profil_metier = Utilisateur.objects.get(email=user_email)
    except (AuthUser.DoesNotExist, Utilisateur.DoesNotExist):
        profil_metier = None
        user_auth = None

    # 3. Récupération des points forts (Maitrise) et points faibles (Besoin)
    points_forts = []
    points_faibles = []
    
    if profil_metier:
        points_forts = Maitrise.objects.filter(utilisateur=profil_metier).select_related('domaine')
        points_faibles = Besoin.objects.filter(utilisateur=profil_metier).select_related('domaine')

    # 4. On envoie le tout au template HTML
    context = {
        'user_django': user_auth,            # Remplace request.user dans le template pour afficher le nom/prénom
        'profil': profil_metier,            # Contient filiere, niveau, photo_profil, bio
        'points_forts': points_forts,        
        'points_faibles': points_faibles,    
    }
    
    return render(request, 'profil.html', context)

def modifier_profil_view(request):
    if not request.user.is_authenticated:
        return redirect('connexion')
    # Cette page affichera le formulaire de modification (modif.html) qu'on verra juste après
    return render(request, 'modif.html')



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
    

def activer_compte_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = AuthUser.objects.get(pk=uid)
        donnees = signing.loads(token, max_age=86400) # Valide 24h
        
        if donnees.get('username') != user.username:
            raise signing.BadSignature
            
    except (TypeError, ValueError, OverflowError, AuthUser.DoesNotExist, signing.SignatureExpired, signing.BadSignature):
        user = None

    if user is not None:
        if not user.is_active:
            # 1. Activation du compte Django dans PostgreSQL
            AuthUser.objects.filter(pk=user.pk).update(is_active=True)
        
        # 2. CRUCIAL : On sauvegarde l'ID de cet utilisateur dans la session 
        # pour s'en souvenir pendant tout le tunnel d'onboarding
        request.session['onboarding_user_id'] = user.id
        
        messages.success(request, "Votre email a été validé ! Complétons votre profil.")
        # 3. Redirection directe vers l'étape de la filière
        return redirect('etape_filiere')
    else:
        return HttpResponse("Le lien d'activation est invalide ou a expiré.", status=400)
    


def etape_filiere_view(request):
    user_id = request.session.get('onboarding_user_id')
    if not user_id:
        messages.error(request, "Accès interdit. Veuillez utiliser le lien d'activation reçu par email.")
        return redirect('connexion')

    # Récupération de l'utilisateur Django
    user_django = AuthUser.objects.get(pk=user_id)

    if request.method == 'POST':
        filiere_choisie = request.POST.get('filiere')
        niveau_choisi = request.POST.get('niveau')

        # --- CORRECTION DIRECTE ICI ---
        # On s'assure de récupérer la vraie valeur du formulaire ou de l'objet AuthUser
        vrai_email = user_django.email if user_django.email else request.POST.get('email')
        
        if not vrai_email:
            # Sécurité si l'email n'est pas trouvé dans l'objet inspecté
            vrai_email = f"user_{user_django.id}@mentoretude.com"

        # Recherche ou création du profil avec le bon email garanti
        utilisateur_custom, created = Utilisateur.objects.get_or_create(
            email=vrai_email,
            defaults={
                'nom': user_django.last_name if user_django.last_name else 'Nom',
                'prenom': user_django.first_name if user_django.first_name else 'Prénom',
                'telephone': f"Non renseigné {user_django.id}",
                'password_hash': user_django.password,
                'filiere': filiere_choisie,
                'niveau': niveau_choisi,
                'actif': True
            }
        )

        if not created:
            utilisateur_custom.filiere = filiere_choisie
            utilisateur_custom.niveau = niveau_choisi
            utilisateur_custom.save()

        # On sauvegarde le vrai email dans la session pour l'étape suivante au cas où
        request.session['verified_user_email'] = vrai_email

        messages.success(request, "Parcours universitaire enregistré.")
        return redirect('etape_maitrise')

    return render(request, 'registration/filiere.html')

def etape_maitrise_view(request):
    user_id = request.session.get('onboarding_user_id') or request.session.get('verified_user_id')
    
    if not user_id:
        messages.error(request, "Veuillez vous connecter pour accéder à cette étape.")
        return redirect('connexion')

    user_django = AuthUser.objects.get(pk=user_id)
    vrai_email = request.session.get('verified_user_email') or user_django.email
    utilisateur_custom = Utilisateur.objects.get(email=vrai_email)

    domaines = Domaine.objects.filter(valide=True).order_by('nom')

    if request.method == 'POST':
        for domaine in domaines:
            statut = request.POST.get(f'statut_{domaine.id}')
            
            # Nettoyage préventif pour éviter les doublons
            Maitrise.objects.filter(utilisateur=utilisateur_custom, domaine=domaine).delete()
            Besoin.objects.filter(utilisateur=utilisateur_custom, domaine=domaine).delete()

            if statut == 'fort':
                niveau_m = request.POST.get(f'niveau_maitrise_{domaine.id}', 'INTERMEDIAIRE')
                Maitrise.objects.create(
                    utilisateur=utilisateur_custom,
                    domaine=domaine,
                    niveau_maitrise=niveau_m
                )
            elif statut == 'faible':
                priorite_b = request.POST.get(f'priorite_{domaine.id}', 3)
                Besoin.objects.create(
                    utilisateur=utilisateur_custom,
                    domaine=domaine,
                    niveau_priorite=int(priorite_b)
                )

        if 'onboarding_user_id' in request.session:
            del request.session['onboarding_user_id']
            messages.success(request, "Votre profil a été configuré avec succès ! Connectez-vous.")
            return redirect('connexion')
        else:
            messages.success(request, "Vos domaines de compétences ont été mis à jour !")
            return redirect('profil')

    # --- SÉLECTION DES DONNÉES EXISTANTES (POUR LE PRÉ-COCHAGE) ---
    # On crée des dictionnaires pour savoir rapidement quel domaine est "fort" ou "faible"
    maitrises_existantes = {m.domaine_id: m for m in Maitrise.objects.filter(utilisateur=utilisateur_custom)}
    besoins_existants = {b.domaine_id: b for b in Besoin.objects.filter(utilisateur=utilisateur_custom)}

    # On prépare une liste de domaines enrichie avec les données de l'utilisateur
    domaines_de_l_utilisateur = []
    for domaine in domaines:
        statut_actuel = 'neutre'
        niveau_actuel = 'INTERMEDIAIRE'
        priorite_actuelle = 3

        if domaine.id in maitrises_existantes:
            statut_actuel = 'fort'
            niveau_actuel = maitrises_existantes[domaine.id].niveau_maitrise
        elif domaine.id in besoins_existants:
            statut_actuel = 'faible'
            priorite_actuelle = besoins_existants[domaine.id].niveau_priorite

        domaines_de_l_utilisateur.append({
            'id': domaine.id,
            'nom': domaine.nom,
            'description': domaine.description,
            'statut_actuel': statut_actuel,
            'niveau_actuel': niveau_actuel,
            'priorite_actuelle': priorite_actuelle,
        })

    context = {
        'domaines_custom': domaines_de_l_utilisateur
    }
    return render(request, 'registration/maitrise.html', context)


def modifier_profil_view(request):
    # Sécurité session : Si l'utilisateur n'est pas connecté dans la session, dehors
    user_email = request.session.get('verified_user_email')
    user_id = request.session.get('verified_user_id')
    
    if not user_email:
        messages.error(request, "Veuillez vous connecter pour accéder à cette page.")
        return redirect('connexion')

    try:
        user_auth = AuthUser.objects.get(id=user_id)
        profil_metier = Utilisateur.objects.get(email=user_email)
    except (AuthUser.DoesNotExist, Utilisateur.DoesNotExist):
        messages.error(request, "Impossible de charger votre profil.")
        return redirect('profil')

    # SI L'UTILISATEUR CLIQUE SUR ENREGISTRER (SOUMISSION DU FORMULAIRE)
    if request.method == 'POST':
        # 1. Récupération des données du formulaire textuel
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telephone = request.POST.get('telephone')
        bio = request.POST.get('bio')

        # 2. Traitement de la photo de profil (Fichier local)
        if request.FILES.get('photo_profil'):
            fichier_image = request.FILES['photo_profil']
            
            # Utilisation du gestionnaire de fichiers de Django pour sauvegarder dans un dossier local
            fs = FileSystemStorage()
            # Sauvegarde l'image dans le sous-dossier 'profil_pics'
            nom_fichier = fs.save(f"profil_pics/user_{user_id}_{fichier_image.name}", fichier_image)
            # Récupère l'URL d'accès au fichier (ex: /media/profil_pics/user_1_image.png)
            url_image = fs.url(nom_fichier)
            
            # Enregistrement du chemin de la photo dans le profil métier
            profil_metier.photo_profil = url_image

        # 3. Sauvegarde des informations textuelles dans AuthUser (via filter + update)
        AuthUser.objects.filter(id=user_id).update(
            first_name=first_name,
            last_name=last_name
        )

        # 4. Sauvegarde dans la table custom 'Utilisateur'
        profil_metier.telephone = telephone
        profil_metier.bio = bio
        profil_metier.save()

        messages.success(request, "Votre profil a été mis à jour avec succès !")
        return redirect('profil')

    # SI L'UTILISATEUR ACCÈDE JUSTE A LA PAGE (AFFICHAGE)
    context = {
        'user_django': user_auth,
        'profil': profil_metier,
    }
    return render(request, 'registration/modif.html', context)

def dashboard_view(request):
    if not request.session.get('verified_user_id'): 
        return redirect('connexion')
    
    # Récupération du profil pour la photo du header
    user_email = request.session.get('verified_user_email')
    profil_metier = Utilisateur.objects.filter(email=user_email).first()
    
    return render(request, 'dashboard.html', {
        'titre_page': 'Dashboard',
        'profil': profil_metier
    })