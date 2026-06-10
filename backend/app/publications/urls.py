from django.urls import path
from . import views
urlpatterns = [
    path('offres/', views.offres_view, name='offres'),
    path('demandes/', views.demandes_view, name='demandes')         
               ]