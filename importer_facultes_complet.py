import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from etudiants.models import Faculte

# ========== LISTE COMPLETE DES FACULTES AU BURUNDI ==========

facultes_completes = [
    # ========== INFORMATIQUE ET TECHNOLOGIE (COMPLET) ==========
    "Génie Informatique",
    "Génie Logiciel",
    "Cybersécurité",
    "Sécurité Informatique",
    "Réseaux Informatiques",
    "Télécommunications",
    "Informatique (Computer Science)",
    "Sciences Informatiques",
    "Informatique de Gestion",
    "Intelligence Artificielle (IA)",
    "Data Science",
    "Science des Données",
    "Développement Web",
    "Développement Mobile",
    "Cloud Computing",
    "DevOps",
    "Blockchain",
    "Robotique",
    "Systèmes Embarqués",
    "Internet des Objets (IoT)",
    "Big Data",
    "Machine Learning",
    "Bioinformatique",
    "Infrastructure et Cloud",
    "Administration des Bases de Données",
    "Architecture des Ordinateurs",
    
    # ========== HOPE AFRICA UNIVERSITY (HAU) ==========
    "Médecine Générale",
    "Chirurgie Dentaire",
    "Anesthésiologie",
    "Ophtalmologie",
    "Soins Infirmiers",
    "Sage-femme (Midwifery)",
    "Kinésithérapie",
    "Nutrition et Diététique",
    "Santé Publique",
    "Génie Civil",
    "Urbanisme et Aménagement",
    "Communication et Journalisme",
    "Comptabilité",
    "Finance et Banque",
    "Marketing",
    "Administration des Entreprises",
    "Entrepreneuriat",
    "Tourisme et Hôtellerie",
    "Droit",
    "Psychologie Clinique",
    "Psychologie Sociale",
    "Travail Social",
    "Développement Communautaire",
    "Théologie",
    "Sciences de l'Éducation",
    "Éducation Spéciale",
    "Enseignement des Langues",
    "Biochimie",
    
    # ========== UNIVERSITE DU BURUNDI (UB) ==========
    "Sciences Economiques",
    "Sciences de Gestion",
    "Droit",
    "Lettres Modernes",
    "Sciences Historiques",
    "Géographie",
    "Mathématiques",
    "Physique",
    "Chimie",
    "Biologie",
    "Médecine",
    "Pharmacie",
    "Psychologie",
    "Sciences de l'Education",
    "Agronomie",
    "Ingénierie",
    "Théologie",
    
    # ========== UNIVERSITE LUMIERE DE BUJUMBURA (ULBU) ==========
    "Gestion des Entreprises",
    "Droit des Affaires",
    "Sciences Infirmières",
    "Sciences Sociales",
    "Sciences de l'Education",
    
    # ========== UNIVERSITE DE NGOZI (UNG) ==========
    "Sciences Economiques et de Gestion",
    "Droit",
    "Sciences Agronomiques",
    "Sciences de l'Education",
    "Lettres et Sciences Humaines",
    
    # ========== UNIVERSITE POLYTECHNIQUE DE GITEGA (UPG) ==========
    "Sciences et Technologies",
    "Ingénierie",
    "Gestion et Economie",
    "Sciences de la Santé",
    "Agriculture et Environnement",
    
    # ========== UNIVERSITE DES GRANDS LACS (UGL) ==========
    "Sciences Economiques",
    "Sciences de Gestion",
    "Droit",
    "Sciences de la Santé",
    
    # ========== UNIVERSITE DU LAC TANGANYIKA ==========
    "Sciences et Technologies",
    "Gestion et Economie",
    "Sciences Sociales",
    "Droit",
    "Sciences de l'Education",
    
    # ========== AUTRES UNIVERSITES ==========
    "Sciences de l'Education (Université de Kirundo)",
    "Sciences Sociales (Université de Kirundo)",
    "Gestion (Université de Kirundo)",
    "Théologie (Université Chrétienne de Bujumbura)",
    "Gestion (Université Chrétienne de Bujumbura)",
    "Informatique (Bujumbura International University)",
    "Gestion (Bujumbura International University)",
    "Droit (Bujumbura International University)",
    "Théologie (Université Martin Luther King)",
    "Sciences de l'Education (Université Martin Luther King)",
]

print("📚 Ajout des facultés...")
print("="*60)

compteur = 0
for f in facultes_completes:
    obj, created = Faculte.objects.get_or_create(nom=f)
    if created:
        compteur += 1
        print(f"✅ {f}")

print("="*60)
print(f"\n🎉 {compteur} nouvelles facultés ajoutées")
print(f"   Total: {Faculte.objects.count()} facultés dans la base")