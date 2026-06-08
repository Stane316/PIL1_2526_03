from django.urls import path
from . import views
urlpatterns = [path('messages/', views.message_view, name='message')]