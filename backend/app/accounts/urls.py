from django.urls import path
from . import views

urlpatterns = [
    path("" , views.home_page_view),
    path('inscription/', views.inscription_view, name='inscription'),
    path("connexion" , views.connexion , name= 'connexion'),
    path("profil/", views.profil, name="profil"),
    path('profil/modifier/', views.modifier_profil_view, name='modifier_profil'),
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie_view, name='password_reset'),
    path('reinitialiser-password/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('activer-compte/<uidb64>/<token>/', views.activer_compte_view, name='activer_compte'),
    path('completer-profil/filiere/', views.etape_filiere_view, name='etape_filiere'),
    path('completer-profil/competences/', views.etape_maitrise_view, name='etape_maitrise'),
]


