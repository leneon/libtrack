"""
Script de configuration des permissions pour LibTrack
Exécute ce script une fois pour configurer tous les rôles
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from livres.models import Livre, Pret, CategorieLivre
from etudiants.models import Etudiant
from etablissement.models import Etablissement

# ==================== 1. CRÉER LES GROUPES ====================

print("📚 Création des groupes...")

# Groupe Super Admin (déjà existe via is_superuser)
super_admin_group, _ = Group.objects.get_or_create(name='Super Administrateur')

# Groupe Administrateur d'établissement
admin_group, created = Group.objects.get_or_create(name='Administrateur')
if created:
    print("✅ Groupe 'Administrateur' créé")

# Groupe Bibliothécaire
bibliothecaire_group, created = Group.objects.get_or_create(name='Bibliothécaire')
if created:
    print("✅ Groupe 'Bibliothécaire' créé")

# ==================== 2. RÉCUPÉRER LES PERMISSIONS ====================

print("\n📚 Récupération des permissions...")

# Permissions pour les ÉTUDIANTS
etudiant_ct = ContentType.objects.get_for_model(Etudiant)
permissions_etudiant = {
    'add_etudiant': Permission.objects.get(codename='add_etudiant', content_type=etudiant_ct),
    'change_etudiant': Permission.objects.get(codename='change_etudiant', content_type=etudiant_ct),
    'delete_etudiant': Permission.objects.get(codename='delete_etudiant', content_type=etudiant_ct),
    'view_etudiant': Permission.objects.get(codename='view_etudiant', content_type=etudiant_ct),
}

# Permissions pour les LIVRES
livre_ct = ContentType.objects.get_for_model(Livre)
permissions_livre = {
    'add_livre': Permission.objects.get(codename='add_livre', content_type=livre_ct),
    'change_livre': Permission.objects.get(codename='change_livre', content_type=livre_ct),
    'delete_livre': Permission.objects.get(codename='delete_livre', content_type=livre_ct),
    'view_livre': Permission.objects.get(codename='view_livre', content_type=livre_ct),
}

# Permissions pour les PRÊTS
pret_ct = ContentType.objects.get_for_model(Pret)
permissions_pret = {
    'add_pret': Permission.objects.get(codename='add_pret', content_type=pret_ct),
    'change_pret': Permission.objects.get(codename='change_pret', content_type=pret_ct),
    'delete_pret': Permission.objects.get(codename='delete_pret', content_type=pret_ct),
    'view_pret': Permission.objects.get(codename='view_pret', content_type=pret_ct),
}

# Permissions pour les CATÉGORIES
categorie_ct = ContentType.objects.get_for_model(CategorieLivre)
permissions_categorie = {
    'add_categorielivre': Permission.objects.get(codename='add_categorielivre', content_type=categorie_ct),
    'change_categorielivre': Permission.objects.get(codename='change_categorielivre', content_type=categorie_ct),
    'delete_categorielivre': Permission.objects.get(codename='delete_categorielivre', content_type=categorie_ct),
    'view_categorielivre': Permission.objects.get(codename='view_categorielivre', content_type=categorie_ct),
}

# Permissions pour les ÉTABLISSEMENTS
etablissement_ct = ContentType.objects.get_for_model(Etablissement)
permissions_etablissement = {
    'add_etablissement': Permission.objects.get(codename='add_etablissement', content_type=etablissement_ct),
    'change_etablissement': Permission.objects.get(codename='change_etablissement', content_type=etablissement_ct),
    'delete_etablissement': Permission.objects.get(codename='delete_etablissement', content_type=etablissement_ct),
    'view_etablissement': Permission.objects.get(codename='view_etablissement', content_type=etablissement_ct),
}

# ==================== 3. CONFIGURER LE GROUPE ADMINISTRATEUR ====================

print("\n👑 Configuration du groupe 'Administrateur'...")

admin_permissions = [
    # Étudiants
    permissions_etudiant['add_etudiant'],
    permissions_etudiant['change_etudiant'],
    permissions_etudiant['view_etudiant'],
    # Livres
    permissions_livre['add_livre'],
    permissions_livre['change_livre'],
    permissions_livre['view_livre'],
    # Prêts
    permissions_pret['add_pret'],
    permissions_pret['change_pret'],
    permissions_pret['view_pret'],
    # Catégories
    permissions_categorie['add_categorielivre'],
    permissions_categorie['change_categorielivre'],
    permissions_categorie['view_categorielivre'],
]

for perm in admin_permissions:
    admin_group.permissions.add(perm)

print(f"✅ {len(admin_permissions)} permissions ajoutées au groupe 'Administrateur'")
print("   - Ajouter/Modifier/Voir les étudiants")
print("   - Ajouter/Modifier/Voir les livres")
print("   - Ajouter/Modifier/Voir les prêts")
print("   - Ajouter/Modifier/Voir les catégories")

# ==================== 4. CONFIGURER LE GROUPE BIBLIOTHÉCAIRE ====================

print("\n📖 Configuration du groupe 'Bibliothécaire'...")

bibliothecaire_permissions = [
    # Étudiants (seulement ajouter et voir)
    permissions_etudiant['add_etudiant'],
    permissions_etudiant['view_etudiant'],
    # Livres (seulement ajouter et voir)
    permissions_livre['add_livre'],
    permissions_livre['view_livre'],
    # Prêts (ajouter, modifier, voir)
    permissions_pret['add_pret'],
    permissions_pret['change_pret'],
    permissions_pret['view_pret'],
    # Catégories (seulement voir)
    permissions_categorie['view_categorielivre'],
]

for perm in bibliothecaire_permissions:
    bibliothecaire_group.permissions.add(perm)

print(f"✅ {len(bibliothecaire_permissions)} permissions ajoutées au groupe 'Bibliothécaire'")
print("   - Ajouter/Voir les étudiants")
print("   - Ajouter/Voir les livres")
print("   - Ajouter/Modifier/Voir les prêts")
print("   - Voir les catégories")

# ==================== 5. METTRE À JOUR LES PROFILS EXISTANTS ====================

print("\n🔄 Mise à jour des profils existants...")

from livres.models import Profile

for profile in Profile.objects.all():
    user = profile.user
    if profile.role == 'super_admin':
        user.is_superuser = True
        user.save()
        print(f"   ✅ {user.username} → Super Admin")
    elif profile.role == 'admin':
        user.groups.add(admin_group)
        user.is_staff = True
        user.save()
        print(f"   ✅ {user.username} → Administrateur")
    elif profile.role == 'bibliothecaire':
        user.groups.add(bibliothecaire_group)
        user.is_staff = True
        user.save()
        print(f"   ✅ {user.username} → Bibliothécaire")

# ==================== 6. CRÉER L'UTILISATEUR SUPER_ADMIN PAR DÉFAUT ====================

print("\n🌟 Création du Super Admin par défaut...")

if not User.objects.filter(username='super_admin').exists():
    super_user = User.objects.create_superuser(
        username='super_admin',
        email='super@libtrack.com',
        password='SuperAdmin2024!'
    )
    profile, _ = Profile.objects.get_or_create(
        user=super_user,
        defaults={'role': 'super_admin'}
    )
    print("✅ Super Admin créé: super_admin / SuperAdmin2024!")
else:
    print("⏭️ Super Admin existe déjà")

print("\n" + "="*50)
print("🎉 CONFIGURATION TERMINÉE !")
print("="*50)
print("\n📋 RÉSUMÉ DES PERMISSIONS :")
print("   ⭐ Super Admin : Accès complet à tout")
print("   👑 Administrateur : Gère sa bibliothèque (ajout, modification)")
print("   📖 Bibliothécaire : Utilise le système (ajout uniquement)")
print("\n🔑 Comptes par défaut :")
print("   super_admin / SuperAdmin2024! (Super Admin)")