import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from etablissement.models import Etablissement

# ========== TOUTES LES UNIVERSITES DU BURUNDI ==========

universites_burundi = [
    # ========== UNIVERSITES PUBLIQUES ==========
    {
        'nom': "Université du Burundi (UB)",
        'code': "UB",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 22 11 11",
        'email': "contact@ub.bi"
    },
    {
        'nom': "Université de Ngozi (UNG)",
        'code': "UNG",
        'adresse': "Ngozi, Burundi",
        'telephone': "+257 22 30 11 11",
        'email': "contact@ung.bi"
    },
    {
        'nom': "Université Polytechnique de Gitega (UPG)",
        'code': "UPG",
        'adresse': "Gitega, Burundi",
        'telephone': "+257 22 40 22 22",
        'email': "info@upg.bi"
    },
    {
        'nom': "Université de l'Environnement de Gitega (UEG)",
        'code': "UEG",
        'adresse': "Gitega, Burundi",
        'telephone': "+257 22 40 33 33",
        'email': "contact@ueg.bi"
    },
    
    # ========== UNIVERSITES PRIVEES ==========
    {
        'nom': "ISGI - Institut Supérieur de Gestion et d'Informatique",
        'code': "ISGI",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 22 22 22",
        'email': "contact@isgi.bi"
    },
    {
        'nom': "ULT - Université de la Technologie",
        'code': "ULT",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 33 33 33",
        'email': "info@ult.bi"
    },
    {
        'nom': "Université Lumière de Bujumbura (ULBU)",
        'code': "ULBU",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 24 44 44",
        'email': "info@ulbu.bi"
    },
    {
        'nom': "Hope Africa University (HAU)",
        'code': "HAU",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 27 77 77",
        'email': "contact@hopeafrica.bi"
    },
    {
        'nom': "Université des Grands Lacs (UGL)",
        'code': "UGL",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 66 66 66",
        'email': "info@ugl.bi"
    },
    {
        'nom': "Université du Lac Tanganyika",
        'code': "ULT-LAC",
        'adresse': "Rumonge, Burundi",
        'telephone': "+257 22 55 55 55",
        'email': "contact@ultlac.bi"
    },
    {
        'nom': "Université de Kirundo (UK)",
        'code': "UK",
        'adresse': "Kirundo, Burundi",
        'telephone': "+257 22 88 88 88",
        'email': "contact@uk.bi"
    },
    {
        'nom': "Université de Mwaro (UM)",
        'code': "UM",
        'adresse': "Mwaro, Burundi",
        'telephone': "+257 22 99 99 99",
        'email': "contact@um.bi"
    },
    {
        'nom': "Université de Rutana (UR)",
        'code': "UR",
        'adresse': "Rutana, Burundi",
        'telephone': "+257 22 77 77 77",
        'email': "contact@ur.bi"
    },
    {
        'nom': "Université de Ruyigi (URY)",
        'code': "URY",
        'adresse': "Ruyigi, Burundi",
        'telephone': "+257 22 44 44 44",
        'email': "contact@ury.bi"
    },
    {
        'nom': "Université de Cankuzo (UC)",
        'code': "UC",
        'adresse': "Cankuzo, Burundi",
        'telephone': "+257 22 55 66 77",
        'email': "contact@uc.bi"
    },
    {
        'nom': "Université de Makamba (UMK)",
        'code': "UMK",
        'adresse': "Makamba, Burundi",
        'telephone': "+257 22 33 44 55",
        'email': "contact@umk.bi"
    },
    {
        'nom': "Université de Bururi (UBU)",
        'code': "UBU",
        'adresse': "Bururi, Burundi",
        'telephone': "+257 22 11 22 33",
        'email': "contact@ubu.bi"
    },
    {
        'nom': "Université de Rumonge (URM)",
        'code': "URM",
        'adresse': "Rumonge, Burundi",
        'telephone': "+257 22 44 55 66",
        'email': "contact@urm.bi"
    },
    
    # ========== INSTITUTS ET ECOLES SUPERIEURES ==========
    {
        'nom': "Institut National de Santé Publique (INSP)",
        'code': "INSP",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 20 20 20",
        'email': "info@insp.bi"
    },
    {
        'nom': "Ecole Normale Supérieure de Bujumbura (ENS)",
        'code': "ENS",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 20 30 40",
        'email': "contact@ens.bi"
    },
    {
        'nom': "Institut des Sciences Agronomiques du Burundi (ISABU)",
        'code': "ISABU",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 20 50 60",
        'email': "info@isabu.bi"
    },
    {
        'nom': "Institut Supérieur de Commerce (ISC)",
        'code': "ISC",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 20 70 80",
        'email': "contact@isc.bi"
    },
    {
        'nom': "Institut Supérieur de Pédagogie Appliquée (ISPA)",
        'code': "ISPA",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 20 90 00",
        'email': "info@ispa.bi"
    },
]

print("📚 Ajout des universités du Burundi...")
print("="*60)

compteur = 0
deja_existantes = 0

for uni in universites_burundi:
    obj, created = Etablissement.objects.get_or_create(
        code=uni['code'],
        defaults={
            'nom': uni['nom'],
            'adresse': uni['adresse'],
            'telephone': uni['telephone'],
            'email': uni['email']
        }
    )
    if created:
        compteur += 1
        print(f"✅ Ajoutée: {uni['nom']} ({uni['code']})")
    else:
        deja_existantes += 1
        print(f"⏭️ Déjà existante: {uni['nom']} ({uni['code']})")

print("="*60)
print(f"\n🎉 Terminé !")
print(f"   - {compteur} universités ajoutées")
print(f"   - {deja_existantes} universités déjà existantes")
print(f"   - Total: {Etablissement.objects.count()} établissements")