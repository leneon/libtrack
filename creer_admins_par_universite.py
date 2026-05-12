import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from django.contrib.auth.models import User
from livres.models import Profile, Etablissement

# ========== RÉCUPÉRER TOUTES LES UNIVERSITÉS ==========
universites = {
    'ISGI': {'code': 'ISGI', 'nom': 'ISGI - Institut Supérieur de Gestion et Informatique'},
    'ULT': {'code': 'ULT', 'nom': 'ULT - Université de la Technologie'},
    'UGL': {'code': 'UGL', 'nom': 'UGL - Université des Grands Lacs'},
    'ULBU': {'code': 'ULBU', 'nom': 'ULBU - Université Lumière de Bujumbura'},
    'UB': {'code': 'UB', 'nom': 'UB - Université du Burundi'},
    'UNG': {'code': 'UNG', 'nom': 'UNG - Université de Ngozi'},
    'UPG': {'code': 'UPG', 'nom': 'UPG - Université Polytechnique de Gitega'},
    'HAU': {'code': 'HAU', 'nom': 'HAU - Hope Africa University'},
    'ULT-LAC': {'code': 'ULT-LAC', 'nom': 'Université du Lac Tanganyika'},
}

# ========== LISTE DES ADMINISTRATEURS À CRÉER ==========
admins = [
    # Super Admin (toi)
    {'username': 'super_admin', 'password': 'Super2024!', 'role': 'super_admin', 'etab_code': None},
    
    # ISGI
    {'username': 'admin_isgi', 'password': 'AdminISGI2024!', 'role': 'admin', 'etab_code': 'ISGI'},
    {'username': 'bib_isgi', 'password': 'BibISGI2024!', 'role': 'bibliothecaire', 'etab_code': 'ISGI'},
    
    # ULT (Université de la Technologie)
    {'username': 'admin_ult', 'password': 'AdminULT2024!', 'role': 'admin', 'etab_code': 'ULT'},
    {'username': 'bib_ult', 'password': 'BibULT2024!', 'role': 'bibliothecaire', 'etab_code': 'ULT'},
    
    # UGL (Université des Grands Lacs)
    {'username': 'admin_ugl', 'password': 'AdminUGL2024!', 'role': 'admin', 'etab_code': 'UGL'},
    {'username': 'bib_ugl', 'password': 'BibUGL2024!', 'role': 'bibliothecaire', 'etab_code': 'UGL'},
    
    # ULBU (Université Lumière de Bujumbura)
    {'username': 'admin_ulbu', 'password': 'AdminULBU2024!', 'role': 'admin', 'etab_code': 'ULBU'},
    {'username': 'bib_ulbu', 'password': 'BibULBU2024!', 'role': 'bibliothecaire', 'etab_code': 'ULBU'},
    
    # UB (Université du Burundi)
    {'username': 'admin_ub', 'password': 'AdminUB2024!', 'role': 'admin', 'etab_code': 'UB'},
    {'username': 'bib_ub', 'password': 'BibUB2024!', 'role': 'bibliothecaire', 'etab_code': 'UB'},
    
    # UNG (Université de Ngozi)
    {'username': 'admin_ung', 'password': 'AdminUNG2024!', 'role': 'admin', 'etab_code': 'UNG'},
    {'username': 'bib_ung', 'password': 'BibUNG2024!', 'role': 'bibliothecaire', 'etab_code': 'UNG'},
    
    # UPG (Université Polytechnique de Gitega)
    {'username': 'admin_upg', 'password': 'AdminUPG2024!', 'role': 'admin', 'etab_code': 'UPG'},
    {'username': 'bib_upg', 'password': 'BibUPG2024!', 'role': 'bibliothecaire', 'etab_code': 'UPG'},
    
    # HAU (Hope Africa University)
    {'username': 'admin_hau', 'password': 'AdminHAU2024!', 'role': 'admin', 'etab_code': 'HAU'},
    {'username': 'bib_hau', 'password': 'BibHAU2024!', 'role': 'bibliothecaire', 'etab_code': 'HAU'},
    
    # ULT-LAC (Université du Lac Tanganyika)
    {'username': 'admin_lac', 'password': 'AdminLAC2024!', 'role': 'admin', 'etab_code': 'ULT-LAC'},
    {'username': 'bib_lac', 'password': 'BibLAC2024!', 'role': 'bibliothecaire', 'etab_code': 'ULT-LAC'},
]

print("="*70)
print("📚 CRÉATION DES ADMINISTRATEURS PAR UNIVERSITÉ")
print("="*70)

compteur = 0
erreurs = 0

for admin in admins:
    try:
        # Récupérer l'établissement
        etab = None
        if admin['etab_code'] and admin['etab_code'] in universites:
            etab, _ = Etablissement.objects.get_or_create(
                code=admin['etab_code'],
                defaults={'nom': universites[admin['etab_code']]['nom']}
            )
        
        # Créer l'utilisateur s'il n'existe pas
        user, created = User.objects.get_or_create(
            username=admin['username'],
            defaults={
                'email': f"{admin['username']}@libtrack.com",
                'first_name': admin['username'].split('_')[1] if '_' in admin['username'] else admin['username'],
                'last_name': admin['role']
            }
        )
        
        if created:
            user.set_password(admin['password'])
            user.save()
        
        # Créer ou mettre à jour le profil
        profile, profile_created = Profile.objects.update_or_create(
            user=user,
            defaults={
                'role': admin['role'],
                'etablissement': etab,
                'telephone': "+257 XX XX XX XX"
            }
        )
        
        # Si super admin, lui donner les droits
        if admin['role'] == 'super_admin':
            user.is_superuser = True
            user.is_staff = True
            user.save()
        else:
            user.is_superuser = False
            user.is_staff = True
            user.save()
        
        compteur += 1
        etab_nom = etab.nom if etab else "Aucun"
        statut = "✅ Créé" if created else "✅ Existe déjà"
        print(f"{statut}: {admin['username']:20} | Mot de passe: {admin['password']:15} | {admin['role']:15} | {etab_nom}")
        
    except Exception as e:
        erreurs += 1
        print(f"❌ Erreur avec {admin['username']}: {str(e)}")

print("="*70)
print(f"\n🎉 {compteur} utilisateurs créés/mis à jour")
print(f"⚠️ {erreurs} erreurs")
print("\n" + "="*70)
print("🔑 RÉSUMÉ DES COMPTES")
print("="*70)

for admin in admins:
    print(f"{admin['username']:20} | {admin['password']:20} | {admin['role']:15} | {universites.get(admin['etab_code'], {}).get('nom', 'Super Admin') if admin['etab_code'] else 'Super Admin'}")

print("\n" + "="*70)
print("📌 POUR SE CONNECTER:")
print("   http://127.0.0.1:8000/login")
print("="*70)