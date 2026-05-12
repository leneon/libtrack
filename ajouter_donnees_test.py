import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from etudiants.models import Etudiant
from livres.models import CategorieLivre, Livre, Pret

# 1. Ajouter une catégorie
categorie, _ = CategorieLivre.objects.get_or_create(nom="Informatique")

# 2. Ajouter un étudiant
etudiant, _ = Etudiant.objects.get_or_create(
    carte_id="ISGI001",
    defaults={
        'nom': "KITARA",
        'prenom': "Jean",
        'classe': "L3 Informatique",
        'faculte': "GL",
        'annee': 3,
        'telephone': "0123456789",
        'email': "jean@isgi.com"
    }
)

# 3. Ajouter un livre
livre, _ = Livre.objects.get_or_create(
    numero_livre="ISGI-BOOK-001",
    defaults={
        'titre': "Django pour les nuls",
        'auteur': "John Doe",
        'emplacement': "Étagère A-12",
        'categorie': categorie,
        'disponible': False
    }
)

# 4. Ajouter un prêt en cours
pret, created = Pret.objects.get_or_create(
    etudiant=etudiant,
    livre=livre,
    defaults={
        'date_emprunt': timezone.now(),
        'date_retour_prevue': timezone.now() + timedelta(days=14),
        'statut': 'emprunte'
    }
)

if created:
    print("✅ Données de test ajoutées !")
else:
    print("⚠️ Les données existent déjà.")