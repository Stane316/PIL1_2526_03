from django.urls import path
from . import views

urlpatterns = [
    path("" , views.home_page_view),
    path('inscription/', views.inscription_view, name='inscription'),
    path("connexion" , views.connexion , name= 'connexion'),
    path("profil/", views.profil, name="profil"),
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie_view, name='password_reset'),
    path('reinitialiser-password/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
]
