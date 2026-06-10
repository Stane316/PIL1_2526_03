from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.message_view, name='message'),
    path('messages/<int:conversation_id>/', views.message_view, name='message_chat'),
    path('messages/contacter/<int:autre_user_id>/', views.démarrer_discussion_view, name='demarrer_chat'),
]