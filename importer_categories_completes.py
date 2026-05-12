import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from livres.models import CategorieLivre
from etablissement.models import Etablissement

# Récupérer l'établissement par défaut (ou créer)
isgi, _ = Etablissement.objects.get_or_create(
    code="ISGI",
    defaults={'nom': "ISGI - Institut Supérieur de Gestion et d'Informatique"}
)

# ========== TOUTES LES CATEGORIES DE LIVRES ==========

categories = [
    # ========== INFORMATIQUE ET TECHNOLOGIE ==========
    "Informatique", "Programmation", "Algorithmique", "Structures de données",
    "Développement Web", "Développement Mobile", "Intelligence Artificielle",
    "Machine Learning", "Data Science", "Big Data", "Cybersécurité", "Réseaux",
    "Cloud Computing", "DevOps", "Base de données", "SQL", "NoSQL",
    "Systèmes d'exploitation", "Linux", "Windows", "Architecture des ordinateurs",
    "Python", "Java", "JavaScript", "C++", "C#", "PHP", "Ruby", "Go", "Rust", "Swift",
    "React", "Angular", "Vue.js", "Django", "Flask", "Spring Boot", "Laravel",
    "Blockchain", "Internet des objets", "Robotique", "Réalité virtuelle",
    
    # ========== MATHÉMATIQUES ET SCIENCES ==========
    "Mathématiques", "Algèbre", "Géométrie", "Analyse", "Calcul", "Probabilités",
    "Statistiques", "Physique", "Mécanique", "Thermodynamique", "Électromagnétisme",
    "Optique", "Physique quantique", "Chimie", "Chimie organique", "Biochimie",
    "Biologie", "Génétique", "Microbiologie", "Botanique", "Zoologie", "Écologie",
    "Neurosciences", "Astronomie", "Cosmologie", "Géologie", "Océanographie",
    
    # ========== MÉDECINE ET SANTÉ ==========
    "Médecine", "Chirurgie", "Cardiologie", "Neurologie", "Pédiatrie", "Gynécologie",
    "Pharmacie", "Pharmacologie", "Sciences infirmières", "Santé publique",
    "Nutrition", "Diététique", "Kinésithérapie", "Psychiatrie", "Dentaire",
    "Vétérinaire", "Biotechnologie médicale", "Imagerie médicale",
    
    # ========== SCIENCES HUMAINES ==========
    "Philosophie", "Éthique", "Psychologie", "Psychologie clinique", "Psychologie sociale",
    "Sociologie", "Anthropologie", "Archéologie", "Histoire", "Géographie",
    "Science politique", "Relations internationales", "Droit", "Droit civil",
    "Droit pénal", "Droit des affaires", "Droit international",
    
    # ========== ÉCONOMIE ET GESTION ==========
    "Économie", "Microéconomie", "Macroéconomie", "Gestion", "Management",
    "Management stratégique", "Management des RH", "Marketing", "Marketing digital",
    "Commerce", "Commerce international", "Finance", "Finance d'entreprise",
    "Banque", "Assurance", "Comptabilité", "Audit", "Logistique", "Supply chain",
    "Entrepreneuriat", "Innovation",
    
    # ========== ARTS, LETTRES ET LANGUES ==========
    "Littérature", "Littérature française", "Littérature africaine", "Poésie",
    "Théâtre", "Roman", "Linguistique", "Grammaire", "Traduction", "Langues",
    "Français", "Anglais", "Espagnol", "Allemand", "Italien", "Portugais",
    "Russe", "Chinois", "Japonais", "Arabe", "Swahili", "Arts plastiques",
    "Dessin", "Peinture", "Photographie", "Cinéma", "Musique", "Architecture",
    "Design", "Design graphique", "Mode",
    
    # ========== SPORT ET BIEN-ÊTRE ==========
    "Sport", "Football", "Basketball", "Tennis", "Natation", "Athlétisme",
    "Arts martiaux", "Yoga", "Fitness", "Musculation", "Développement personnel",
    "Bien-être", "Méditation", "Coaching", "Motivation", "Cuisine", "Œnologie",
    "Voyage", "Tourisme",
    
    # ========== RELIGION ET SPIRITUALITÉ ==========
    "Christianisme", "Bible", "Théologie", "Islam", "Coran", "Judaïsme",
    "Bouddhisme", "Hindouisme", "Spiritualité",
    
    # ========== JEUNESSE ET ÉDUCATION ==========
    "Littérature jeunesse", "Albums illustrés", "Contes", "Bande dessinée",
    "Manga", "Comics", "Pédagogie", "Éducation", "Enseignement", "Méthodologie",
    
    # ========== TECHNIQUE ET INDUSTRIE ==========
    "Génie civil", "Bâtiment", "Construction", "Génie électrique", "Électricité",
    "Électronique", "Génie mécanique", "Mécanique", "Aéronautique", "Automobile",
    "Génie chimique", "Génie industriel", "Génie environnemental", "Énergie",
    "Énergies renouvelables", "Agriculture", "Agronomie",
    
    # ========== DICTIONNAIRES ET ENCYCLOPÉDIES ==========
    "Dictionnaires", "Encyclopédies", "Atlas", "Guides pratiques",
]

print("="*60)
print("📚 AJOUT DES CATEGORIES DE LIVRES")
print("="*60)

compteur = 0
for cat in categories:
    obj, created = CategorieLivre.objects.get_or_create(
        nom=cat,
        etablissement=isgi
    )
    if created:
        compteur += 1
        if compteur % 20 == 0:
            print(f"   ✅ {compteur} catégories ajoutées...")

print("="*60)
print(f"\n🎉 Terminé ! {compteur} catégories ajoutées sur {len(categories)}")
print(f"   Total: {CategorieLivre.objects.count()} catégories")