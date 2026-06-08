from django.shortcuts import render
from django.shortcuts import render, redirect
from app.core.models import Utilisateur


# Create your views here.

def message_view(request):
    if not request.session.get('verified_user_id'): return redirect('connexion')
    user_email = request.session.get('verified_user_email')
    profil_metier = Utilisateur.objects.filter(email=user_email).first()
    return render(request, 'message.html', {'titre_page': 'Messages', 'profil': profil_metier})
