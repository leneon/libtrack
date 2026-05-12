from django.db import models
from django.contrib.auth.models import User
from etablissement.models import Etablissement

# NOUVEAU MODELE POUR FACULTE
class Faculte(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Faculté"
        verbose_name_plural = "Facultés"

class Etudiant(models.Model):
    FACULTES = [
        ('GL', 'Génie Logiciel'),
        ('IIA', 'Informatique et Intelligence Artificielle'),
        ('RSD', 'Réseaux et Sécurité Digitale'),
        ('MF', 'Management Financier'),
        ('MKG', 'Marketing Digital'),
        ('RH', 'Ressources Humaines'),
        ('LOG', 'Logistique et Transport'),
        ('CG', 'Comptabilité et Gestion'),
        ('ECM', 'Économie et Commerce International'),
        ('JUR', 'Droit des Affaires'),
        ('COMM', 'Communication Digitale'),
        ('ENT', 'Entrepreneuriat'),
    ]
    
    ANNEES_ACADEMIQUES = [
        (2020, '2020'),
        (2021, '2021'),
        (2022, '2022'),
        (2023, '2023'),
        (2024, '2024'),
        (2025, '2025'),
        (2026, '2026'),
        (2027, '2027'),
        (2028, '2028'),
        (2029, '2029'),
        (2030, '2030'),
    ]
    
    NIVEAUX = [
        (1, 'L1 (1ère année)'),
        (2, 'L2 (2ème année)'),
        (3, 'L3 (3ème année)'),
        (4, 'M1 (Master 1)'),
        (5, 'M2 (Master 2)'),
        (6, 'Doctorat (PhD)'),
        (7, 'Licence Professionnelle'),
        (8, 'Bachelor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    classe = models.CharField(max_length=100, help_text="Ex: L3 Informatique, M1 Gestion")
    faculte = models.ForeignKey(Faculte, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Faculté")
    niveau = models.IntegerField(choices=NIVEAUX, default=3, verbose_name="Niveau d'étude")
    annee_academique = models.IntegerField(choices=ANNEES_ACADEMIQUES, default=2026, verbose_name="Année académique")
    carte_id = models.CharField(max_length=50, unique=True)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.classe} ({self.annee_academique})"