from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('non-rendus/', views.non_rendus, name='non_rendus'),
    path('historique/', views.historique, name='historique'),
    path('retourner/<int:pret_id>/', views.retourner, name='retourner'),
    path('recherche/', views.recherche_livres, name='recherche_livres'),
    path('categorie/<int:categorie_id>/', views.livres_par_categorie, name='livres_par_categorie'),
    path('tous-les-livres/', views.tous_les_livres, name='tous_les_livres'),
    path('ajouter-livre/', views.ajouter_livre, name='ajouter_livre'),
    path('ajouter-etudiant/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('liste-etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('creer-pret/', views.creer_pret, name='creer_pret'),
]