# tasks.py
import os
from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
from django.conf import settings
from .models import Offre  # Import du modèle Offre
from celery import shared_task

@shared_task
def envoyer_candidature_email(nom, message, cv_path, offre_titre):
    # Obtenez l'offre en fonction du titre
    offre = Offre.objects.filter(titre=offre_titre).first()
    
    if not offre:
        return

    subject = f'Nouvelle candidature pour l\'offre "{offre.titre}"'
    # Créez le contenu de l'email en texte brut
    message_body = f"Nom : {nom}\nMessage : {message}\nPoste : {offre.titre}"

    destinataire_email = os.getenv('DESTINATAIRE_EMAIL')
    email = EmailMessage(
        subject,
        message_body,
        settings.DEFAULT_FROM_EMAIL,
        [destinataire_email],
    )
   # Attacher le CV en utilisant le chemin du fichier
    with open(cv_path, 'rb') as f:
        email.attach(os.path.basename(cv_path), f.read(), 'application/pdf')

    email.send()
