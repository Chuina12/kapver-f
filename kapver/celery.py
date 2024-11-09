from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configurez les paramètres Django pour que Celery puisse les utiliser.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapver.settings')

app = Celery('kapver-final-v2')

# Charger les configurations de Celery à partir du fichier settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découverte automatique des tâches dans tous les fichiers tasks.py de vos apps
app.autodiscover_tasks()
