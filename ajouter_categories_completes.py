import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from livres.models import CategorieLivre
from etablissement.models import Etablissement

# Récupérer l'établissement ISGI (ou créer par défaut)
isgi, _ = Etablissement.objects.get_or_create(
    code="ISGI",
    defaults={'nom': "ISGI - Institut Supérieur de Gestion et d'Informatique"}
)

# ==================== TOUTES LES CATÉGORIES DE LIVRES ====================

categories = [
    # ========== 1. INFORMATIQUE ET TECHNOLOGIE ==========
    "Informatique", "Programmation", "Algorithmique", "Structures de données",
    "Développement Web", "Développement Mobile", "Développement Desktop",
    "Intelligence Artificielle", "Machine Learning", "Deep Learning", "Data Science",
    "Big Data", "Cybersécurité", "Réseaux informatiques", "Cloud Computing",
    "DevOps", "Base de données", "SQL", "NoSQL", "Systèmes d'exploitation",
    "Linux", "Windows", "Unix", "Architecture des ordinateurs", "Compilation",
    "Langages de programmation", "Python", "Java", "JavaScript", "C++", "C#",
    "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "HTML/CSS",
    "React", "Angular", "Vue.js", "Django", "Flask", "Spring Boot", "Laravel",
    "Node.js", "Blockchain", "Internet des objets", "Robotique", "Réalité virtuelle",
    "Réalité augmentée", "Impression 3D", "Bureautique", "Microsoft Office",
    "Excel", "Word", "PowerPoint", "Photoshop", "Illustrator", "After Effects",
    
    # ========== 2. MATHÉMATIQUES ET SCIENCES ==========
    "Mathématiques", "Algèbre", "Géométrie", "Analyse mathématique", "Calcul différentiel",
    "Calcul intégral", "Équations différentielles", "Probabilités", "Statistiques",
    "Mathématiques appliquées", "Mathématiques discrètes", "Logique mathématique",
    "Théorie des nombres", "Topologie", "Physique", "Mécanique", "Thermodynamique",
    "Électromagnétisme", "Optique", "Physique quantique", "Physique nucléaire",
    "Astrophysique", "Chimie", "Chimie organique", "Chimie inorganique",
    "Chimie analytique", "Chimie physique", "Biochimie", "Biologie", "Biologie cellulaire",
    "Biologie moléculaire", "Génétique", "Microbiologie", "Botanique", "Zoologie",
    "Écologie", "Neurosciences", "Anatomie", "Physiologie", "Sciences de la Terre",
    "Géologie", "Océanographie", "Météorologie", "Astronomie", "Cosmologie",
    
    # ========== 3. MÉDECINE ET SANTÉ ==========
    "Médecine générale", "Médecine interne", "Cardiologie", "Neurologie", "Pédiatrie",
    "Gynécologie", "Obstétrique", "Chirurgie", "Orthopédie", "Ophtalmologie",
    "ORL", "Dermatologie", "Urologie", "Psychiatrie", "Anesthésie", "Radiologie",
    "Pharmacie", "Pharmacologie", "Toxicologie", "Sciences infirmières", "Soins infirmiers",
    "Santé publique", "Épidémiologie", "Nutrition", "Diététique", "Physiothérapie",
    "Kinésithérapie", "Ergothérapie", "Orthophonie", "Dentaire", "Chirurgie dentaire",
    "Vétérinaire", "Médecine vétérinaire", "Biotechnologie médicale", "Imagerie médicale",
    "Urgences médicales", "Gériatrie", "Pneumologie", "Gastroentérologie", "Néphrologie",
    "Endocrinologie", "Rhumatologie", "Hématologie", "Oncologie", "Infectiologie",
    
    # ========== 4. SCIENCES HUMAINES ET SOCIALES ==========
    "Philosophie", "Métaphysique", "Éthique", "Esthétique", "Logique", "Épistémologie",
    "Psychologie", "Psychologie clinique", "Psychologie cognitive", "Psychologie sociale",
    "Psychologie du développement", "Psychanalyse", "Sociologie", "Anthropologie",
    "Ethnologie", "Archéologie", "Histoire", "Histoire ancienne", "Histoire médiévale",
    "Histoire moderne", "Histoire contemporaine", "Géographie", "Géographie physique",
    "Géographie humaine", "Cartographie", "Science politique", "Relations internationales",
    "Géopolitique", "Droit", "Droit civil", "Droit pénal", "Droit des affaires",
    "Droit du travail", "Droit international", "Droit constitutionnel", "Droit fiscal",
    "Sciences de l'éducation", "Pédagogie", "Didactique", "Éducation spécialisée",
    "Psychopédagogie", "Communication", "Journalisme", "Médias", "Publicité",
    
    # ========== 5. ÉCONOMIE, GESTION ET FINANCE ==========
    "Économie", "Microéconomie", "Macroéconomie", "Économétrie", "Économie internationale",
    "Économie du développement", "Gestion", "Management", "Management stratégique",
    "Management des ressources humaines", "Marketing", "Marketing digital", "Commerce",
    "Commerce international", "Vente", "Négociation", "Finance", "Finance d'entreprise",
    "Finance de marché", "Banque", "Assurance", "Comptabilité", "Comptabilité générale",
    "Comptabilité analytique", "Audit", "Contrôle de gestion", "Logistique", "Supply chain",
    "Achats", "Transport", "Entrepreneuriat", "Innovation", "Création d'entreprise",
    
    # ========== 6. ARTS, LETTRES ET LANGUES ==========
    "Littérature", "Littérature française", "Littérature africaine", "Littérature américaine",
    "Littérature anglaise", "Littérature arabe", "Littérature asiatique", "Poésie",
    "Théâtre", "Roman", "Nouvelle", "Essai", "Critique littéraire", "Linguistique",
    "Grammaire", "Orthographe", "Syntaxe", "Sémantique", "Phonétique", "Traduction",
    "Interprétariat", "Langues", "Français", "Anglais", "Espagnol", "Allemand",
    "Italien", "Portugais", "Russe", "Chinois", "Japonais", "Coréen", "Arabe",
    "Hébreu", "Latin", "Grec ancien", "Swahili", "Lingala", "Kinyarwanda",
    "Arts plastiques", "Dessin", "Peinture", "Sculpture", "Gravure", "Photographie",
    "Cinéma", "Réalisation", "Scénario", "Montage", "Musique", "Solfège", "Instruments",
    "Chant", "Composition", "Histoire de l'art", "Architecture", "Design", "Design graphique",
    "Design d'intérieur", "Design de mode", "Mode", "Stylisme", "Couture",
    
    # ========== 7. SPORT, LOISIRS ET BIEN-ÊTRE ==========
    "Sport", "Football", "Basketball", "Tennis", "Natation", "Athlétisme", "Cyclisme",
    "Sports de combat", "Arts martiaux", "Judo", "Karaté", "Boxe", "Yoga", "Fitness",
    "Musculation", "Course à pied", "Randonnée", "Escalade", "Alpinisme", "Ski",
    "Snowboard", "Surf", "Voile", "Pêche", "Chasse", "Jeux", "Échecs", "Jeux de société",
    "Jeux vidéo", "E-sport", "Loisirs créatifs", "Cuisine", "Pâtisserie", "Œnologie",
    "Voyage", "Tourisme", "Hôtellerie", "Restauration", "Développement personnel",
    "Bien-être", "Méditation", "Relaxation", "Sophrologie", "Coaching", "Motivation",
    "Bonheur", "Relations", "Parentalité", "Sexualité",
    
    # ========== 8. RELIGION, SPIRITUALITÉ ET PHILOSOPHIE DE VIE ==========
    "Christianisme", "Bible", "Théologie", "Islam", "Coran", "Judaïsme", "Bouddhisme",
    "Hindouisme", "Spiritualité", "Ésotérisme", "Mysticisme", "Astrologie", "Numérologie",
    "Feng Shui", "Médiumnité", "Paranormal", "Franc-maçonnerie", "Symbolisme",
    
    # ========== 9. JEUNESSE, ENFANCE ET ÉDUCATION ==========
    "Littérature jeunesse", "Albums illustrés", "Contes", "Fables", "Comptines",
    "Bande dessinée", "Manga", "Comics", "Livres d'activités", "Coloriage",
    "Jeux éducatifs", "Éveil", "Petite enfance", "Adolescence", "Scolaire", "Manuels scolaires",
    "Préparation examens", "Concours", "Orientation scolaire", "Méthodologie",
    
    # ========== 10. TECHNIQUE, BÂTIMENT ET INDUSTRIE ==========
    "Génie civil", "Bâtiment", "Construction", "Travaux publics", "Architecture",
    "Urbanisme", "Génie électrique", "Électricité", "Électronique", "Automatisme",
    "Robotique", "Génie mécanique", "Mécanique", "Thermique", "Fluides", "Aéronautique",
    "Automobile", "Génie chimique", "Génie industriel", "Génie environnemental",
    "Énergie", "Énergies renouvelables", "Pétrole", "Gaz", "Mines", "Agronomie",
    "Agriculture", "Élevage", "Foresterie", "Environnement", "Écologie appliquée",
    
    # ========== 11. DICTIONNAIRES, ENCYCLOPÉDIES ET OUVRAGES DE RÉFÉRENCE ==========
    "Dictionnaires", "Dictionnaire de langue", "Dictionnaire bilingue",
    "Dictionnaire thématique", "Encyclopédies", "Atlas", "Guides pratiques",
    "Annuaires", "Codes", "Lois", "Règlements", "Normes", "Catalogues",
    
    # ========== 12. ACTUALITÉS, POLITIQUE ET SOCIÉTÉ ==========
    "Actualités", "Politique", "Géopolitique", "Société", "Écologie", "Environnement",
    "Droits de l'homme", "Droits des femmes", "Égalité", "Diversité", "Inclusion",
    "Mondialisation", "Développement durable", "Décolonisation", "Post-colonialisme",
    
    # ========== 13. SCIENCES DE L'INFORMATION ET DOCUMENTATION ==========
    "Bibliothéconomie", "Archivistique", "Documentation", "Gestion de l'information",
    "Classification", "Catalogage", "Indexation", "Numérisation", "Bibliothèques numériques",
    "Veille informationnelle", "Gestion des connaissances",
    
    # ========== 14. ARMÉE, DÉFENSE ET SECOURS ==========
    "Armée", "Défense", "Stratégie militaire", "Tactique", "Histoire militaire",
    "Sécurité", "Sécurité civile", "Pompiers", "Secourisme", "Premiers secours",
    "Protection civile", "Crise", "Gestion des catastrophes", "Sauvetage",
    
    # ========== 15. MÉTIERS ET FORMATION PROFESSIONNELLE ==========
    "Métiers", "Formation professionnelle", "Artisanat", "Bricolage", "Jardinage",
    "Couture", "Tricot", "Broderie", "Menuiserie", "Serrurerie", "Plomberie",
    "Électricité bâtiment", "Maçonnerie", "Peinture en bâtiment", "Cuisine professionnelle",
    "Pâtisserie professionnelle", "Boulangerie", "Charcuterie", "Service en salle",
    "Hôtellerie", "Tourisme", "Coiffure", "Esthétique", "Onglerie", "Maquillage",
]

print("📚 Ajout des catégories de livres...")
compteur = 0

for cat in categories:
    obj, created = CategorieLivre.objects.get_or_create(
        nom=cat,
        etablissement=isgi
    )
    if created:
        compteur += 1
        if compteur % 50 == 0:
            print(f"   ✅ {compteur} catégories ajoutées...")

print(f"\n🎉 Terminé ! {compteur} catégories ajoutées sur {len(categories)} totales.")
print(f"\n📋 Exemple de catégories disponibles:")
print("   - Informatique, Programmation, Intelligence Artificielle")
print("   - Médecine, Pharmacie, Psychologie")
print("   - Littérature, Philosophie, Histoire")
print("   - Marketing, Finance, Management")
print("   - Sport, Cuisine, Développement personnel")