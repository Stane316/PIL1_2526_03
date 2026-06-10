from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.message_view, name='message'),
    path('messages/api/<int:conv_id>/', views.message_api_view, name='message_api'),
    path('messages/api/<int:conv_id>/envoyer/', views.envoyer_message_api, name='envoyer_message_api'),
]
