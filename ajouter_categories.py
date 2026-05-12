import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from livres.models import CategorieLivre

categories = [
    # Sciences humaines et sociales
    "Philosophie", "Psychologie", "Sociologie", "Anthropologie", "Histoire", "Géographie", 
    "Science politique", "Droit", "Économie", "Gestion", "Communication", "Journalisme",
    
    # Sciences exactes et naturelles
    "Mathématiques", "Physique", "Chimie", "Biologie", "Sciences de la Terre", "Astronomie", 
    "Informatique", "Intelligence artificielle", "Data science", "Réseaux informatiques",
    "Programmation", "Cybersécurité", "Robotique", "Électronique", "Mécanique",
    
    # Sciences de la vie et santé
    "Médecine", "Pharmacie", "Dentaire", "Vétérinaire", "Sciences infirmières", 
    "Nutrition", "Santé publique", "Biotechnologie", "Génétique", "Neurosciences",
    
    # Arts, lettres et langues
    "Littérature française", "Littérature étrangère", "Poésie", "Théâtre", 
    "Français", "Anglais", "Espagnol", "Allemand", "Italien", "Arabe", "Chinois", 
    "Linguistique", "Traduction", "Arts plastiques", "Musique", "Cinéma", "Photographie",
    "Architecture", "Design", "Mode", "Cuisine", "Œnologie",
    
    # Éducation et formation
    "Pédagogie", "Éducation", "Formation professionnelle", "Petite enfance",
    "Enseignement supérieur", "Recherche", "Méthodologie",
    
    # Techniques et ingénierie
    "Génie civil", "Génie électrique", "Génie mécanique", "Génie chimique", 
    "Génie industriel", "Génie logiciel", "Génie environnemental", "Aéronautique",
    "Automobile", "Énergie", "Bâtiment", "Transport", "Logistique", "Qualité",
    
    # Commerce et finance
    "Marketing", "Vente", "Commerce international", "Finance", "Comptabilité", 
    "Audit", "Contrôle de gestion", "Ressources humaines", "Management", 
    "Entrepreneuriat", "Supply chain", "Achats", "Négociation",
    
    # Sport et loisirs
    "Sport", "Fitness", "Yoga", "Arts martiaux", "Jeux", "Échecs", "E-sport",
    "Randonnée", "Camping", "Voyage", "Tourisme", "Hôtellerie", "Restauration",
    
    # Religion et spiritualité
    "Christianisme", "Islam", "Judaïsme", "Bouddhisme", "Hindouisme", "Spiritualité",
    "Théologie", "Ésotérisme", "Méditation",
    
    # Dictionnaires et encyclopédies
    "Dictionnaires", "Encyclopédies", "Atlas", "Guides pratiques", "Annnuaires",
    
    # Bandes dessinées et jeunesse
    "Bande dessinée", "Manga", "Comics", "Littérature jeunesse", "Contes", "Fables",
    "Albums illustrés", "Coloriage", "Activités manuelles",
    
    # Développement personnel
    "Développement personnel", "Bien-être", "Coaching", "Motivation", "Réussite",
    "Bonheur", "Relations", "Parentalité",
]

print(f"📚 Ajout des catégories de livres...")
compteur = 0

for cat in categories:
    obj, created = CategorieLivre.objects.get_or_create(nom=cat)
    if created:
        compteur += 1
        print(f"   ✅ Ajoutée : {cat}")
    else:
        print(f"   ⏭️ Déjà existante : {cat}")

print(f"\n🎉 Terminé ! {compteur} nouvelles catégories ajoutées sur {len(categories)} totales.")