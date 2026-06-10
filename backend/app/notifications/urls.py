from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/api/', views.notifications_api_view, name='notifications_api'),
]
