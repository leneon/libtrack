from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from livres.models import Profile
from etablissement.models import Etablissement
import random

CITATIONS = [
    ("Une bibliothèque, c'est une maison où l'on soigne les âmes.", "Anonyme"),
    ("Les bibliothèques sont les archives de l'humanité.", "Jorge Luis Borges"),
]

def page_accueil(request):
    citation = random.choice(CITATIONS)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'accueil.html', {'error': 'Identifiants incorrects', 'citation': citation})
    
    return render(request, 'accueil.html', {'citation': citation})

def is_super_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'super_admin')

@login_required
@user_passes_test(is_super_admin)
def ajouter_utilisateur(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email', '')
        prenom = request.POST.get('prenom', '')
        nom = request.POST.get('nom', '')
        telephone = request.POST.get('telephone', '')
        etablissement_id = request.POST.get('etablissement')
        role = request.POST.get('role')
        
        if not username or not password:
            messages.error(request, '❌ Nom d\'utilisateur et mot de passe requis')
            return redirect('ajouter_utilisateur')
        
        if password != password2:
            messages.error(request, '❌ Les mots de passe ne correspondent pas')
            return redirect('ajouter_utilisateur')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'❌ L\'utilisateur "{username}" existe déjà')
            return redirect('ajouter_utilisateur')
        
        user = User.objects.create_user(username=username, email=email, password=password, first_name=prenom, last_name=nom)
        
        etablissement = None
        if etablissement_id:
            try:
                etablissement = Etablissement.objects.get(id=etablissement_id)
            except:
                pass
        
        Profile.objects.create(user=user, etablissement=etablissement, role=role, telephone=telephone)
        
        messages.success(request, f'✅ Utilisateur "{username}" créé')
        return redirect('liste_utilisateurs')
    
    etablissements = Etablissement.objects.all()
    return render(request, 'ajouter_utilisateur.html', {'etablissements': etablissements})

@login_required
@user_passes_test(is_super_admin)
def liste_utilisateurs(request):
    utilisateurs = User.objects.all().select_related('profile')
    return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})