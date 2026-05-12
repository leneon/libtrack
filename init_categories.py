import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque_isgi.settings')
django.setup()

from livres.models import Etablissement, CategorieLivre

# 1. Créer l'établissement ISGI par défaut
etablissement, created = Etablissement.objects.get_or_create(
    code="ISGI",
    defaults={
        'nom': "ISGI - Institut Supérieur de Gestion et d'Informatique",
        'adresse': "Bujumbura, Burundi",
        'telephone': "+257 22 22 22 22",
        'email': "contact@isgi.bi"
    }
)
print(f"✅ Établissement: {etablissement.nom}")

# 2. Liste complète des catégories de livres (50+ catégories)
categories = [
    # Informatique
    "Informatique", "Programmation", "Développement Web", "Développement Mobile",
    "Intelligence Artificielle", "Machine Learning", "Data Science", "Big Data",
    "Cybersécurité", "Réseaux", "Cloud Computing", "DevOps", "Base de données",
    "Systèmes d'exploitation", "Algorithmique", "Langages de programmation",
    
    # Sciences
    "Mathématiques", "Physique", "Chimie", "Biologie", "Sciences de la Terre",
    "Astronomie", "Génétique", "Biotechnologie", "Neurosciences",
    
    # Santé
    "Médecine", "Pharmacie", "Dentaire", "Vétérinaire", "Sciences infirmières",
    "Nutrition", "Santé publique", "Psychologie", "Psychiatrie",
    
    # Sciences humaines
    "Philosophie", "Sociologie", "Anthropologie", "Histoire", "Géographie",
    "Archéologie", "Politique", "Droit", "Économie", "Gestion", "Marketing",
    "Ressources Humaines", "Finance", "Comptabilité", "Logistique", "Commerce",
    
    # Arts et lettres
    "Littérature", "Poésie", "Théâtre", "Cinéma", "Musique", "Peinture",
    "Photographie", "Architecture", "Design", "Mode",
    
    # Langues
    "Français", "Anglais", "Espagnol", "Allemand", "Italien", "Arabe", "Chinois",
    "Linguistique", "Traduction",
    
    # Développement personnel
    "Développement personnel", "Coaching", "Motivation", "Bien-être", "Méditation",
    "Spiritualité", "Yoga", "Fitness",
    
    # Jeunesse et BD
    "Bande dessinée", "Manga", "Comics", "Littérature jeunesse", "Contes",
    
    # Autres
    "Cuisine", "Voyage", "Sport", "Cuisine", "Jardinage", "Bricolage",
]

# 3. Ajouter toutes les catégories
compteur = 0
for cat in categories:
    obj, created = CategorieLivre.objects.get_or_create(
        nom=cat,
        etablissement=etablissement
    )
    if created:
        compteur += 1
        print(f"   📚 Ajoutée: {cat}")

print(f"\n🎉 Terminé ! {compteur} catégories ajoutées sur {len(categories)} totales.")
print(f"\n💡 Connecte-toi avec: admin / admin123")
print(f"📚 Pour ajouter un livre: http://127.0.0.1:8000/admin/livres/livre/add/")