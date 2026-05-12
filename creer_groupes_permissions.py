import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from livres.models import Livre, Pret, CategorieLivre
from etudiants.models import Etudiant, Faculte
from etablissement.models import Etablissement

print("="*60)
print("📚 CREATION DES GROUPES ET PERMISSIONS")
print("="*60)

# 1. Créer les groupes
groupe_super_admin, _ = Group.objects.get_or_create(name='Super Admin')
groupe_admin_etablissement, _ = Group.objects.get_or_create(name='Administrateur Etablissement')
groupe_bibliothecaire, _ = Group.objects.get_or_create(name='Bibliothécaire')

print("\n✅ Groupes créés:")
print(f"   - Super Admin (accès complet)")
print(f"   - Administrateur Etablissement (gestion de son etablissement)")
print(f"   - Bibliothécaire (utilisation simple)")

# 2. Récupérer tous les content types
ct_etudiant = ContentType.objects.get_for_model(Etudiant)
ct_faculte = ContentType.objects.get_for_model(Faculte)
ct_livre = ContentType.objects.get_for_model(Livre)
ct_pret = ContentType.objects.get_for_model(Pret)
ct_categorie = ContentType.objects.get_for_model(CategorieLivre)
ct_etablissement = ContentType.objects.get_for_model(Etablissement)

# 3. Définir les permissions par groupe
print("\n" + "="*60)
print("📋 PERMISSIONS PAR GROUPE")
print("="*60)

# ========== GROUPE SUPER ADMIN (toutes les permissions) ==========
# Le Super Admin gère via is_superuser, pas besoin d'ajouter des permissions
print("\n👑 SUPER ADMIN:")
print("   - Accès complet à toutes les fonctionnalités")
print("   - Voit tous les établissements")
print("   - Peut tout faire")

# ========== GROUPE ADMINISTRATEUR ETABLISSEMENT ==========
permissions_admin = [
    # Etudiants
    Permission.objects.get(codename='add_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='change_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='delete_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='view_etudiant', content_type=ct_etudiant),
    
    # Livres
    Permission.objects.get(codename='add_livre', content_type=ct_livre),
    Permission.objects.get(codename='change_livre', content_type=ct_livre),
    Permission.objects.get(codename='delete_livre', content_type=ct_livre),
    Permission.objects.get(codename='view_livre', content_type=ct_livre),
    
    # Prets
    Permission.objects.get(codename='add_pret', content_type=ct_pret),
    Permission.objects.get(codename='change_pret', content_type=ct_pret),
    Permission.objects.get(codename='delete_pret', content_type=ct_pret),
    Permission.objects.get(codename='view_pret', content_type=ct_pret),
    
    # Categories
    Permission.objects.get(codename='add_categorielivre', content_type=ct_categorie),
    Permission.objects.get(codename='change_categorielivre', content_type=ct_categorie),
    Permission.objects.get(codename='view_categorielivre', content_type=ct_categorie),
]

for perm in permissions_admin:
    groupe_admin_etablissement.permissions.add(perm)

print(f"\n👨‍💼 ADMINISTRATEUR ETABLISSEMENT:")
print(f"   - {len(permissions_admin)} permissions ajoutées")
print("   - Peut: Ajouter/Modifier/Supprimer/Voir les étudiants")
print("   - Peut: Ajouter/Modifier/Supprimer/Voir les livres")
print("   - Peut: Ajouter/Modifier/Supprimer/Voir les prêts")
print("   - Peut: Gérer les catégories")

# ========== GROUPE BIBLIOTHECAIRE ==========
permissions_bibliothecaire = [
    # Etudiants (seulement ajouter et voir)
    Permission.objects.get(codename='add_etudiant', content_type=ct_etudiant),
    Permission.objects.get(codename='view_etudiant', content_type=ct_etudiant),
    
    # Livres (seulement ajouter et voir)
    Permission.objects.get(codename='add_livre', content_type=ct_livre),
    Permission.objects.get(codename='view_livre', content_type=ct_livre),
    
    # Prets (ajouter, modifier comme rendu, voir)
    Permission.objects.get(codename='add_pret', content_type=ct_pret),
    Permission.objects.get(codename='change_pret', content_type=ct_pret),
    Permission.objects.get(codename='view_pret', content_type=ct_pret),
    
    # Categories (seulement voir)
    Permission.objects.get(codename='view_categorielivre', content_type=ct_categorie),
]

for perm in permissions_bibliothecaire:
    groupe_bibliothecaire.permissions.add(perm)

print(f"\n📖 BIBLIOTHECAIRE:")
print(f"   - {len(permissions_bibliothecaire)} permissions ajoutées")
print("   - Peut: Ajouter/Voir les étudiants")
print("   - Peut: Ajouter/Voir les livres")
print("   - Peut: Ajouter/Modifier/Voir les prêts")
print("   - Peut: Voir les catégories")

print("\n" + "="*60)
print("🎉 CONFIGURATION TERMINEE !")
print("="*60)
print("\nPour utiliser ces groupes:")
print("   1. Allez dans /admin/auth/user/")
print("   2. Ajoutez ou modifiez un utilisateur")
print("   3. Dans la section 'Groupes', selectionnez le groupe voulu")