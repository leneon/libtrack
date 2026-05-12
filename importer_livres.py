import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from livres.models import Livre, CategorieLivre, Etablissement

# Livres à importer (tu peux ajouter des milliers)
livres_data = [
    {"numero": "ISGI-001", "titre": "Python pour les nuls", "auteur": "John Doe", "isbn": "978-1234567890", "editeur": "Eyrolles", "annee": 2023, "emplacement": "A-12", "categorie": "Informatique"},
    {"numero": "ISGI-002", "titre": "Django Masterclass", "auteur": "Jane Smith", "isbn": "978-0987654321", "editeur": "O'Reilly", "annee": 2024, "emplacement": "B-05", "categorie": "Informatique"},
    {"numero": "ISGI-003", "titre": "Data Science avec Python", "auteur": "Alan Turing", "isbn": "978-1122334455", "editeur": "Pearson", "annee": 2022, "emplacement": "C-08", "categorie": "Informatique"},
    # Ajoute autant de livres que tu veux ici
]

etablissement, _ = Etablissement.objects.get_or_create(code="ISGI", defaults={'nom': "ISGI - Institut Supérieur..."})

for data in livres_data:
    categorie, _ = CategorieLivre.objects.get_or_create(nom=data['categorie'], etablissement=etablissement)
    livre, created = Livre.objects.get_or_create(
        numero_livre=data['numero'],
        defaults={
            'titre': data['titre'],
            'auteur': data['auteur'],
            'isbn': data['isbn'],
            'editeur': data['editeur'],
            'annee_publication': data['annee'],
            'emplacement': data['emplacement'],
            'categorie': categorie,
            'etablissement': etablissement,
            'quantite_totale': 1,
            'quantite_disponible': 1,
            'disponible': True,
        }
    )
    if created:
        print(f"✅ Ajouté: {data['titre']}")
    else:
        print(f"⏭️ Déjà existant: {data['titre']}")

print("\n🎉 Import terminé !")