from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core import signing
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, logout, authenticate  # IMPORTATION DES SESSIONS NATIVES DE DJANGO
from django.contrib.auth.models import User

from app.core.models import AuthUser, Utilisateur, Domaine, Maitrise, Besoin
from .forms import InscriptionForm, ConnexionForm, DemandeReinitialisationForm, NouveauMotDePasseForm

def inscription_view(request):
    """
    Vue d'inscription fluide (Étape 1).
    Pour simplifier l'onboarding locaux (soutenance), l'utilisateur est activé
    immédiatement et redirigé de manière asynchrone et automatique vers l'Étape 2 (La filière).
    """
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # 1. Hachage du mot de passe
            user.password = make_password(form.cleaned_data['password'])
            
            # 2. Remplir les contraintes NOT NULL de PostgreSQL
            user.is_superuser = False
            user.is_staff = False
            user.date_joined = timezone.now()
            user.is_active = True  # Activé immédiatement pour un onboarding direct et sans friction !
            user.save()
            
            # Sauvegarde temporaire du téléphone dans la session pour l'onboarding profil
            request.session['temp_telephone'] = request.POST.get('telephone', '')
            
            # Authentification et connexion automatique
            login(request, user)
            request.session['verified_user_id'] = user.id
            request.session['verified_user_email'] = user.email
            request.session['onboarding_user_id'] = user.id
            
            messages.success(request, "Compte créé ! Complétons votre parcours universitaire.")
            return redirect('etape_filiere')  # Redirection directe vers l'Étape 2 !
    else:
        form = InscriptionForm()
    return render(request, 'registration/inscription.html', {'form': form})

def home_page_view(request):
    return render(request ,"home.html")


def connexion(request):
    """
    Vue de connexion unifiée et sécurisée.
    Transition hybride : Utilise l'authentification native de Django (contrib.auth.login)
    tout en préservant les variables de session manuelles pour garantir 100% de compatibilité.
    """
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authentification native via Django
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if not user.is_active:
                    messages.error(request, "Votre compte n'est pas encore activé. Vérifiez vos emails.")
                    return render(request, "registration/login.html", {'form': form})
                
                # Connexion de la session native Django (request.user sera maintenant peuplé)
                login(request, user)
                
                # Sauvegarde des variables manuelles de session pour la compatibilité
                request.session['verified_user_id'] = user.id
                request.session['verified_user_email'] = user.email
                request.session['username'] = user.username
                
                return redirect('profil')
            else:
                messages.error(request, "Identifiants ou mot de passe incorrects.")
    else:
        form = ConnexionForm()
        
    return render(request, "registration/login.html", {'form': form})


def deconnexion_view(request):
    """
    Déconnexion propre de la session utilisateur.
    Vide la session Django native et flashe toutes les variables de session manuelles.
    """
    logout(request)
    request.session.flush()  # Nettoie intégralement la session
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('connexion')


def profil(request):
    # Sécurité hybride : double vérification session manuelle ou authentification native Django
    user_id = request.session.get('verified_user_id') or (request.user.id if request.user.is_authenticated else None)
    
    if not user_id:
        messages.error(request, "Veuillez vous connecter pour accéder à votre profil.")
        return redirect('connexion')

    try:
        user_auth = AuthUser.objects.get(id=user_id)
        profil_metier = Utilisateur.objects.get(email=user_auth.email)
    except (AuthUser.DoesNotExist, Utilisateur.DoesNotExist):
        profil_metier = None
        user_auth = None

    # Récupération des points forts (Maitrise) et points faibles (Besoin)
    points_forts = []
    points_faibles = []
    
    if profil_metier:
        points_forts = Maitrise.objects.filter(utilisateur=profil_metier).select_related('domaine')
        points_faibles = Besoin.objects.filter(utilisateur=profil_metier).select_related('domaine')

    context = {
        'user_django': user_auth,
        'profil': profil_metier,
        'points_forts': points_forts,        
        'points_faibles': points_faibles,    
    }
    
    return render(request, 'profil.html', context)


def mot_de_passe_oublie_view(request):
    if request.method == 'POST':
        form = DemandeReinitialisationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = AuthUser.objects.filter(email=email).first()
                if user is None:
                    raise AuthUser.DoesNotExist
                
                token = signing.dumps({'username': user.username})
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                domaine = request.get_host()
                lien = f"http://{domaine}/reinitialiser-password/{uid}/{token}/"
                
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


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = AuthUser.objects.get(pk=uid)
        donnees = signing.loads(token, max_age=7200)
        
        if donnees.get('username') != user.username:
            raise signing.BadSignature
            
    except (TypeError, ValueError, OverflowError, AuthUser.DoesNotExist, signing.SignatureExpired, signing.BadSignature):
        user = None

    if user is not None:
        if request.method == 'POST':
            form = NouveauMotDePasseForm(request.POST)
            if form.is_valid():
                nouveau_hash = make_password(form.cleaned_data['password']) 
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
        donnees = signing.loads(token, max_age=86400)
        
        if donnees.get('username') != user.username:
            raise signing.BadSignature
            
    except (TypeError, ValueError, OverflowError, AuthUser.DoesNotExist, signing.SignatureExpired, signing.BadSignature):
        user = None

    if user is not None:
        if not user.is_active:
            AuthUser.objects.filter(pk=user.pk).update(is_active=True)
        
        request.session['onboarding_user_id'] = user.id
        messages.success(request, "Votre email a été validé ! Complétons votre profil.")
        return redirect('etape_filiere')
    else:
        return HttpResponse("Le lien d'activation est invalide ou a expiré.", status=400)
    

def etape_filiere_view(request):
    user_id = request.session.get('onboarding_user_id')
    if not user_id:
        messages.error(request, "Accès interdit. Veuillez utiliser le lien d'activation reçu par email.")
        return redirect('connexion')

    user_django = AuthUser.objects.get(pk=user_id)

    if request.method == 'POST':
        filiere_choisie = request.POST.get('filiere')
        niveau_choisi = request.POST.get('niveau')

        vrai_email = user_django.email if user_django.email else request.POST.get('email')
        if not vrai_email:
            vrai_email = f"user_{user_django.id}@mentoretude.com"

        # Récupération sécurisée du téléphone saisi à l'Étape 1 d'inscription
        tel_saisi = request.session.get('temp_telephone') or f"Non renseigné {user_django.id}"

        # Recherche ou création du profil avec le bon email garanti
        utilisateur_custom, created = Utilisateur.objects.get_or_create(
            email=vrai_email,
            defaults={
                'nom': user_django.last_name if user_django.last_name else 'Nom',
                'prenom': user_django.first_name if user_django.first_name else 'Prénom',
                'telephone': tel_saisi,
                'password_hash': user_django.password,
                'filiere': filiere_choisie,
                'niveau': niveau_choisi,
                'actif': True
            }
        )

        if not created:
            utilisateur_custom.filiere = filiere_choisie
            utilisateur_custom.niveau = niveau_choisi
            utilisateur_custom.telephone = tel_saisi
            utilisateur_custom.save()

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
            # On log l'utilisateur pour qu'il arrive directement sur son dashboard après onboarding !
            login(request, user_django)
            request.session['verified_user_id'] = user_django.id
            request.session['verified_user_email'] = user_django.email
            messages.success(request, "Votre profil a été configuré avec succès ! Bienvenue sur MentorLink.")
            return redirect('dashboard')
        else:
            messages.success(request, "Vos domaines de compétences ont été mis à jour !")
            return redirect('profil')

    maitrises_existantes = {m.domaine_id: m for m in Maitrise.objects.filter(utilisateur=utilisateur_custom)}
    besoins_existants = {b.domaine_id: b for b in Besoin.objects.filter(utilisateur=utilisateur_custom)}

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

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telephone = request.POST.get('telephone')
        bio = request.POST.get('bio')

        if request.FILES.get('photo_profil'):
            fichier_image = request.FILES['photo_profil']
            fs = FileSystemStorage()
            nom_fichier = fs.save(f"profil_pics/user_{user_id}_{fichier_image.name}", fichier_image)
            url_image = fs.url(nom_fichier)
            profil_metier.photo_profil = url_image

        AuthUser.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name)
        profil_metier.telephone = telephone
        profil_metier.bio = bio
        profil_metier.save()

        messages.success(request, "Votre profil a été mis à jour avec succès !")
        return redirect('profil')

    context = {
        'user_django': user_auth,
        'profil': profil_metier,
    }
    return render(request, 'registration/modif.html', context)


def dashboard_view(request):
    if not request.session.get('verified_user_id'): 
        return redirect('connexion')
    
    user_email = request.session.get('verified_user_email')
    profil_metier = Utilisateur.objects.filter(email=user_email).first()
    
    return render(request, 'dashboard.html', {
        'titre_page': 'Dashboard',
        'profil': profil_metier
    })
