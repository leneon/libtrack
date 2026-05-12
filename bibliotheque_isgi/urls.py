from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import page_accueil, ajouter_utilisateur, liste_utilisateurs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', page_accueil, name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include('livres.urls')),
    path('ajouter-utilisateur/', ajouter_utilisateur, name='ajouter_utilisateur'),
    path('utilisateurs/', liste_utilisateurs, name='liste_utilisateurs'),
]