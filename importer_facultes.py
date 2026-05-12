import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from etudiants.models import Faculte

facultes = [
    "Génie Logiciel",
    "Informatique et Intelligence Artificielle",
    "Réseaux et Sécurité Digitale",
    "Management Financier",
    "Marketing Digital",
    "Ressources Humaines",
    "Logistique et Transport",
    "Comptabilité et Gestion",
    "Économie et Commerce International",
    "Droit des Affaires",
    "Communication Digitale",
    "Entrepreneuriat",
]

print("📚 Ajout des facultés...")
compteur = 0

for f in facultes:
    obj, created = Faculte.objects.get_or_create(nom=f)
    if created:
        compteur += 1
        print(f"✅ Ajoutée: {f}")
    else:
        print(f"⏭️ Déjà existante: {f}")

print(f"\n🎉 Terminé ! {compteur} facultés ajoutées.")