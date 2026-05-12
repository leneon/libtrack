import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from livres.models import Profile
from etudiants.models import Etudiant
from livres.models import Livre, Pret, CategorieLivre

print("="*60)
print("🔧 CORRECTION DES PERMISSIONS")
print("="*60)

# Récupérer les groupes
groupe_admin, _ = Group.objects.get_or_create(name='Administrateur Etablissement')
groupe_bibliothecaire, _ = Group.objects.get_or_create(name='Bibliothécaire')

# Récupérer les permissions
ct_etudiant = ContentType.objects.get_for_model(Etudiant)
ct_livre = ContentType.objects.get_for_model(Livre)
ct_pret = ContentType.objects.get_for_model(Pret)
ct_categorie = ContentType.objects.get_for_model(CategorieLivre)

# Permissions pour ADMIN
permissions_admin = [
    Permission.objects.get(codename='add_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='change_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='delete_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='view_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='add_livre', content_type=ct_livre),
    Permission.objects.get(codename='change_livre', content_type=ct_livre),
    Permission.objects.get(codename='delete_livre', content_type=ct_livre),
    Permission.objects.get(codename='view_livre', content_type=ct_livre),
    Permission.objects.get(codename='add_pret', content_type=ct_pret),
    Permission.objects.get(codename='change_pret', content_type=ct_pret),
    Permission.objects.get(codename='delete_pret', content_type=ct_pret),
    Permission.objects.get(codename='view_pret', content_type=ct_pret),
    Permission.objects.get(codename='add_categorielivre', content_type=ct_categorie),
    Permission.objects.get(codename='change_categorielivre', content_type=ct_categorie),
    Permission.objects.get(codename='view_categorielivre', content_type=ct_categorie),
]

# Permissions pour BIBLIOTHECAIRE
permissions_bib = [
    Permission.objects.get(codename='add_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='view_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='add_livre', content_type=ct_livre),
    Permission.objects.get(codename='view_livre', content_type=ct_livre),
    Permission.objects.get(codename='add_pret', content_type=ct_pret),
    Permission.objects.get(codename='change_pret', content_type=ct_pret),
    Permission.objects.get(codename='view_pret', content_type=ct_pret),
    Permission.objects.get(codename='view_categorielivre', content_type=ct_categorie),
]

# Vider les permissions existantes des groupes
groupe_admin.permissions.clear()
groupe_bibliothecaire.permissions.clear()

# Ajouter les nouvelles permissions
for perm in permissions_admin:
    groupe_admin.permissions.add(perm)

for perm in permissions_bib:
    groupe_bibliothecaire.permissions.add(perm)

print(f"✅ Groupe 'Administrateur' a {groupe_admin.permissions.count()} permissions")
print(f"✅ Groupe 'Bibliothécaire' a {groupe_bibliothecaire.permissions.count()} permissions")

# Assigner les groupes aux utilisateurs
for profile in Profile.objects.all():
    user = profile.user
    if profile.role == 'super_admin':
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"✅ {user.username} → Super Admin")
    elif profile.role == 'admin':
        user.groups.add(groupe_admin)
        user.is_superuser = False
        user.is_staff = True
        user.save()
        print(f"✅ {user.username} → Administrateur (groupes: {list(user.groups.all())})")
    elif profile.role == 'bibliothecaire':
        user.groups.add(groupe_bibliothecaire)
        user.is_superuser = False
        user.is_staff = True
        user.save()
        print(f"✅ {user.username} → Bibliothécaire")

print("\n" + "="*60)
print("🎉 CORRECTION TERMINÉE !")
print("="*60)