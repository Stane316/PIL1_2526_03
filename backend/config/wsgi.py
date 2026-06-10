import os

from django.core.wsgi import get_wsgi_application

# Remplace 'config.settings' par le chemin de tes paramètres si nécessaire, 
# mais normalement si ton dossier s'appelle 'config', c'est exactement ça.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()