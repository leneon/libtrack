from django.db import models
from django.contrib.auth.models import User
from etablissement.models import Etablissement

class Profile(models.Model):
    """Profil utilisateur pour lier un utilisateur à un établissement"""
    ROLE_CHOICES = (
        ('super_admin', 'Super Administrateur'),
        ('admin', 'Administrateur d\'établissement'),
        ('bibliothecaire', 'Bibliothécaire'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    etablissement = models.ForeignKey(Etablissement, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='bibliothecaire')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class CategorieLivre(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nom

class Livre(models.Model):
    numero_livre = models.CharField(max_length=50)
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    emplacement = models.CharField(max_length=100, default="A-01")
    categorie = models.ForeignKey(CategorieLivre, on_delete=models.SET_NULL, null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    editeur = models.CharField(max_length=100, blank=True, null=True)
    annee_publication = models.IntegerField(blank=True, null=True)
    resume = models.TextField(blank=True, null=True)
    quantite_totale = models.IntegerField(default=1)
    quantite_disponible = models.IntegerField(default=1)
    disponible = models.BooleanField(default=True)
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['numero_livre', 'etablissement']
    
    def __str__(self):
        return f"[{self.etablissement.code}] {self.titre}"

class Pret(models.Model):
    STATUT_CHOICES = (
        ('emprunte', 'Emprunté'),
        ('rendu', 'Rendu'),
    )
    
    etudiant = models.ForeignKey('etudiants.Etudiant', on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour_prevue = models.DateTimeField()
    date_retour_reelle = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='emprunte')
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.etudiant.nom} - {self.livre.titre}"