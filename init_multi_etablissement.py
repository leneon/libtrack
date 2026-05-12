import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from django.contrib.auth.models import User
from etablissement.models import Etablissement
from livres.models import Profile, CategorieLivre

# 1. Créer l'établissement ISGI
isgi, created = Etablissement.objects.get_or_create(
    code="ISGI",
    defaults={
        'nom': "ISGI - Institut Supérieur de Gestion et d'Informatique",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 22 22 22",
        'email': "contact@isgi.bi"
    }
)
print(f"✅ Établissement: {isgi.nom}")

# 2. Créer le super admin (toi)
if not User.objects.filter(username='super_admin').exists():
    super_user = User.objects.create_superuser(
        username='super_admin',
        email='super@libtrack.com',
        password='SuperAdmin2024!'
    )
    profile = Profile.objects.create(
        user=super_user,
        role='super_admin',
        etablissement=None
    )
    print("✅ Super admin créé: super_admin / SuperAdmin2024!")
else:
    print("⏭️ Super admin existe déjà")

# 3. Créer un admin pour ISGI
if not User.objects.filter(username='admin_isgi').exists():
    admin_isgi = User.objects.create_user(
        username='admin_isgi',
        email='admin@isgi.bi',
        password='AdminISGI2024!'
    )
    profile = Profile.objects.create(
        user=admin_isgi,
        role='admin',
        etablissement=isgi
    )
    print("✅ Admin ISGI créé: admin_isgi / AdminISGI2024!")
else:
    print("⏭️ Admin ISGI existe déjà")

# 4. Créer un bibliothécaire pour ISGI
if not User.objects.filter(username='bib_isgi').exists():
    bib_isgi = User.objects.create_user(
        username='bib_isgi',
        email='bib@isgi.bi',
        password='BibISGI2024!'
    )
    profile = Profile.objects.create(
        user=bib_isgi,
        role='bibliothecaire',
        etablissement=isgi
    )
    print("✅ Bibliothécaire ISGI créé: bib_isgi / BibISGI2024!")
else:
    print("⏭️ Bibliothécaire ISGI existe déjà")

# 5. Ajouter des catégories par défaut pour ISGI
categories = [
    "Informatique", "Programmation", "Intelligence Artificielle", 
    "Marketing", "Finance", "Développement personnel", "Management",
    "Mathématiques", "Physique", "Chimie", "Biologie"
]

for cat in categories:
    obj, created = CategorieLivre.objects.get_or_create(
        nom=cat,
        etablissement=isgi
    )
    if created:
        print(f"   📚 Catégorie ajoutée: {cat}")

print("\n🎉 Configuration multi-établissements terminée !")
print("\n🔑 Accès:")
print("   Super Admin: super_admin / SuperAdmin2024!")
print("   Admin ISGI: admin_isgi / AdminISGI2024!")
print("   Biblio ISGI: bib_isgi / BibISGI2024!")