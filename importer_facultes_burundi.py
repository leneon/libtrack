import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from etudiants.models import Faculte

# ========== TOUTES LES FACULTES DU BURUNDI ==========

facultes_burundi = [
    # ========== UNIVERSITE DU BURUNDI (UB) ==========
    "Faculté des Sciences Economiques et Administratives",
    "Faculté de Droit",
    "Faculté des Lettres et Sciences Humaines",
    "Faculté des Sciences",
    "Faculté de Médecine",
    "Faculté de Pharmacie",
    "Faculté de Psychologie et Sciences de l'Education",
    "Faculté d'Agronomie et de Bio-Ingénierie",
    "Faculté d'Ingénierie",
    "Faculté de Théologie",
    
    # ========== UNIVERSITE LUMIERE DE BUJUMBURA (ULBU) ==========
    "Faculté de Gestion et Administration des Entreprises",
    "Faculté de Droit et Sciences Politiques",
    "Faculté des Sciences de la Santé",
    "Faculté des Sciences Sociales",
    "Faculté d'Informatique",
    "Faculté des Sciences de l'Education",
    
    # ========== UNIVERSITE DE NGOZI (UNG) ==========
    "Faculté des Sciences Economiques et de Gestion",
    "Faculté de Droit",
    "Faculté des Sciences Agronomiques",
    "Faculté des Sciences de l'Education",
    "Faculté des Lettres et Sciences Humaines",
    
    # ========== UNIVERSITE POLYTECHNIQUE DE GITEGA (UPG) ==========
    "Faculté des Sciences et Technologies",
    "Faculté des Sciences de l'Ingénieur",
    "Faculté de Gestion et Economie",
    "Faculté des Sciences de la Santé",
    "Faculté d'Agriculture et Environnement",
    
    # ========== HOPE AFRICA UNIVERSITY (HAU) ==========
    "Faculté de Médecine",
    "Faculté de Pharmacie",
    "Faculté des Sciences Infirmières",
    "Faculté de Santé Publique",
    "Faculté de Gestion et Développement",
    "Faculté des Sciences Sociales",
    "Faculté de Théologie",
    
    # ========== UNIVERSITE DU LAC TANGANYIKA (ULT) ==========
    "Faculté des Sciences et Technologies",
    "Faculté de Gestion et Economie",
    "Faculté des Sciences Sociales",
    "Faculté de Droit",
    "Faculté des Sciences de l'Education",
    
    # ========== UNIVERSITE DES GRANDS LACS (UGL) ==========
    "Faculté des Sciences Economiques",
    "Faculté des Sciences de Gestion",
    "Faculté de Droit",
    "Faculté des Sciences Informatiques",
    "Faculté des Sciences de la Santé",
    
    # ========== AUTRES ETABLISSEMENTS ==========
    "Faculté des Sciences Infirmières et Obstétricales",
    "Faculté de Santé et Développement",
    "Faculté des Sciences et Techniques de l'Information",
    "Faculté de Journalisme et Communication",
    "Faculté des Arts et Culture",
    "Faculté de Musique et Arts Dramatiques",
    "Faculté des Sciences du Sport",
    "Faculté de Tourisme et Hôtellerie",
    "Faculté des Sciences Vétérinaires",
    "Faculté d'Architecture et Urbanisme",
    "Faculté des Mines et Géologie",
    "Faculté des Energies Renouvelables",
    "Faculté de Biochimie",
    "Faculté de Biotechnologie",
    "Faculté de Microbiologie",
    
    # ========== INFORMATIQUE ET TECHNOLOGIE ==========
    "Faculté de Génie Logiciel",
    "Faculté de Cyber sécurité",
    "Faculté de Data Science",
    "Faculté d'Intelligence Artificielle",
    "Faculté de Développement Web et Mobile",
    "Faculté de Cloud Computing",
    "Faculté de Réseaux et Télécommunications",
    "Faculté de Robotique",
    "Faculté de Systèmes Embarqués",
    
    # ========== GESTION ET COMMERCE ==========
    "Faculté de Management",
    "Faculté de Marketing",
    "Faculté de Finance et Banque",
    "Faculté de Comptabilité",
    "Faculté d'Audit et Contrôle",
    "Faculté de Management des Ressources Humaines",
    "Faculté de Logistique",
    "Faculté de Commerce International",
    "Faculté d'Entrepreneuriat",
    
    # ========== SCIENCES HUMAINES ==========
    "Faculté de Psychologie",
    "Faculté de Sociologie",
    "Faculté d'Anthropologie",
    "Faculté d'Histoire",
    "Faculté de Géographie",
    "Faculté de Philosophie",
    "Faculté de Langues Etrangères",
    "Faculté de Linguistique",
    "Faculté de Traduction et Interprétariat",
    
    # ========== SCIENCES FONDAMENTALES ==========
    "Faculté de Mathématiques",
    "Faculté de Physique",
    "Faculté de Chimie",
    "Faculté de Biologie",
    "Faculté de Sciences de la Terre",
    "Faculté de Géologie",
    "Faculté d'Ecologie",
]

print("📚 Ajout des facultés du Burundi...")
print("="*50)

compteur = 0
deja_existantes = 0

for f in facultes_burundi:
    obj, created = Faculte.objects.get_or_create(nom=f)
    if created:
        compteur += 1
        print(f"✅ Ajoutée: {f}")
    else:
        deja_existantes += 1

print("="*50)
print(f"\n🎉 Terminé !")
print(f"   - {compteur} facultés ajoutées")
print(f"   - {deja_existantes} facultés déjà existantes")
print(f"   - Total: {Faculte.objects.count()} facultés")