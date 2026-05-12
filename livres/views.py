from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models
from django.db.models import Count, Q
from collections import defaultdict
from .models import Livre, Pret, CategorieLivre, Profile
from etudiants.models import Etudiant
from etablissement.models import Etablissement

def get_user_etablissement(request):
    """Récupère l'établissement de l'utilisateur connecté"""
    if hasattr(request.user, 'profile') and request.user.profile.etablissement:
        return request.user.profile.etablissement
    return None

@login_required
def accueil(request):
    etablissement = get_user_etablissement(request)
    maintenant = timezone.now()
    
    # Filtrer par établissement
    if request.user.is_superuser:
        prets = Pret.objects.filter(statut='emprunte').select_related('etudiant', 'livre')
        total_etudiants = Etudiant.objects.count()
        livres_disponibles = Livre.objects.filter(disponible=True).count()
        livres_recents = Livre.objects.all().order_by('-date_ajout')[:8]
        categories = CategorieLivre.objects.all()
        total_livres = Livre.objects.count()
    else:
        prets = Pret.objects.filter(statut='emprunte', etablissement=etablissement).select_related('etudiant', 'livre')
        total_etudiants = Etudiant.objects.filter(etablissement=etablissement).count()
        livres_disponibles = Livre.objects.filter(disponible=True, etablissement=etablissement).count()
        livres_recents = Livre.objects.filter(etablissement=etablissement).order_by('-date_ajout')[:8]
        categories = CategorieLivre.objects.filter(etablissement=etablissement)
        total_livres = Livre.objects.filter(etablissement=etablissement).count()
    
    prets_count = prets.count()
    prets_retard = sum(1 for p in prets if p.date_retour_prevue and p.date_retour_prevue < maintenant)
    
    # Traitement du retour
    if request.method == 'POST' and 'pret_id' in request.POST:
        pret_id = request.POST.get('pret_id')
        pret = get_object_or_404(Pret, id=pret_id)
        pret.statut = 'rendu'
        pret.date_retour_reelle = timezone.now()
        pret.save()
        
        livre = pret.livre
        livre.disponible = True
        livre.quantite_disponible += 1
        livre.save()
        
        messages.success(request, f'✅ Livre "{livre.titre}" retourné')
        return redirect('accueil')
    
    # Catégories avec comptage
    livres_par_categorie = []
    for cat in categories:
        if request.user.is_superuser:
            count = Livre.objects.filter(categorie=cat).count()
        else:
            count = Livre.objects.filter(categorie=cat, etablissement=etablissement).count()
        if count > 0:
            livres_par_categorie.append({'nom': cat.nom, 'count': count, 'id': cat.id})
    
    # ========== DONNÉES POUR LES GRAPHIQUES ==========
    
    # 1. Prêts par catégorie
    categories_graph = CategorieLivre.objects.annotate(nb_pret=Count('livre__pret')).filter(nb_pret__gt=0)
    if not request.user.is_superuser:
        categories_graph = categories_graph.filter(etablissement=etablissement)
    
    categories_labels = [cat.nom for cat in categories_graph]
    categories_data = [cat.nb_pret for cat in categories_graph]
    
    # 2. Évolution des prêts (7 derniers jours)
    evolution_labels = []
    evolution_data = []
    for i in range(6, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        evolution_labels.append(date.strftime('%d/%m'))
        if request.user.is_superuser:
            count = Pret.objects.filter(date_emprunt__date=date).count()
        else:
            count = Pret.objects.filter(date_emprunt__date=date, etablissement=etablissement).count()
        evolution_data.append(count)
    
    # 3. Livres les plus empruntés
    if request.user.is_superuser:
        livres_populaires = Livre.objects.annotate(nb_emprunts=Count('pret')).filter(nb_emprunts__gt=0).order_by('-nb_emprunts')[:5]
    else:
        livres_populaires = Livre.objects.filter(etablissement=etablissement).annotate(nb_emprunts=Count('pret')).filter(nb_emprunts__gt=0).order_by('-nb_emprunts')[:5]
    
    total_emprunts = sum(l.nb_emprunts for l in livres_populaires)
    for livre in livres_populaires:
        livre.percent = round((livre.nb_emprunts / total_emprunts) * 100) if total_emprunts > 0 else 0
    
    return render(request, 'livres/accueil.html', {
        'prets': prets,
        'now': maintenant,
        'total_etudiants': total_etudiants,
        'livres_disponibles': livres_disponibles,
        'prets_count': prets_count,
        'prets_retard': prets_retard,
        'livres_recents': livres_recents,
        'livres_par_categorie': livres_par_categorie,
        'total_livres': total_livres,
        'categories_labels': categories_labels,
        'categories_data': categories_data,
        'evolution_labels': evolution_labels,
        'evolution_data': evolution_data,
        'livres_populaires': livres_populaires,
    })

@login_required
def tous_les_livres(request):
    etablissement = get_user_etablissement(request)
    
    if request.user.is_superuser:
        livres = Livre.objects.all().order_by('-date_ajout')
        categories = CategorieLivre.objects.all()
    else:
        livres = Livre.objects.filter(etablissement=etablissement).order_by('-date_ajout')
        categories = CategorieLivre.objects.filter(etablissement=etablissement)
    
    return render(request, 'livres/tous_les_livres.html', {
        'livres': livres,
        'categories': categories,
        'total': livres.count(),
        'disponibles': livres.filter(disponible=True).count(),
        'empruntes': livres.filter(disponible=False).count(),
    })

@login_required
def ajouter_livre(request):
    etablissement = get_user_etablissement(request)
    
    if request.method == 'POST':
        numero_livre = request.POST.get('numero_livre')
        titre = request.POST.get('titre')
        auteur = request.POST.get('auteur')
        categorie_id = request.POST.get('categorie')
        emplacement = request.POST.get('emplacement')
        
        if not numero_livre or not titre or not auteur:
            messages.error(request, '❌ Numéro, Titre et Auteur sont obligatoires')
            return redirect('ajouter_livre')
        
        if Livre.objects.filter(numero_livre=numero_livre, etablissement=etablissement).exists():
            messages.error(request, f'❌ Le numéro "{numero_livre}" existe déjà')
            return redirect('ajouter_livre')
        
        categorie = None
        if categorie_id:
            try:
                categorie = CategorieLivre.objects.get(id=categorie_id, etablissement=etablissement)
            except:
                pass
        
        Livre.objects.create(
            numero_livre=numero_livre,
            titre=titre,
            auteur=auteur,
            categorie=categorie,
            emplacement=emplacement or 'A-01',
            etablissement=etablissement,
            quantite_totale=1,
            quantite_disponible=1,
            disponible=True
        )
        
        messages.success(request, f'✅ Livre "{titre}" ajouté')
        return redirect('tous_les_livres')
    
    categories = CategorieLivre.objects.filter(etablissement=etablissement) if etablissement else CategorieLivre.objects.all()
    return render(request, 'livres/ajouter_livre.html', {'categories': categories})

@login_required
def ajouter_etudiant(request):
    etablissement = get_user_etablissement(request)
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        classe = request.POST.get('classe')
        faculte = request.POST.get('faculte')
        carte_id = request.POST.get('carte_id')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email', '')
        
        if not nom or not prenom or not carte_id:
            messages.error(request, '❌ Nom, Prénom et Carte ID sont obligatoires')
            return redirect('ajouter_etudiant')
        
        if Etudiant.objects.filter(carte_id=carte_id, etablissement=etablissement).exists():
            messages.error(request, f'❌ La carte "{carte_id}" existe déjà')
            return redirect('ajouter_etudiant')
        
        Etudiant.objects.create(
            nom=nom,
            prenom=prenom,
            classe=classe or 'Non spécifié',
            faculte=faculte or 'GL',
            carte_id=carte_id,
            telephone=telephone or '',
            email=email,
            etablissement=etablissement
        )
        
        messages.success(request, f'✅ Étudiant "{nom} {prenom}" ajouté')
        return redirect('liste_etudiants')
    
    return render(request, 'livres/ajouter_etudiant.html')

@login_required
def liste_etudiants(request):
    etablissement = get_user_etablissement(request)
    
    if request.user.is_superuser:
        etudiants = Etudiant.objects.all()
    else:
        etudiants = Etudiant.objects.filter(etablissement=etablissement)
    
    return render(request, 'livres/liste_etudiants.html', {'etudiants': etudiants})

@login_required
def creer_pret(request):
    etablissement = get_user_etablissement(request)
    
    if request.method == 'POST':
        carte_id = request.POST.get('carte_id')
        livre_id = request.POST.get('livre_id')
        date_retour = request.POST.get('date_retour')
        
        try:
            etudiant = Etudiant.objects.get(carte_id=carte_id, etablissement=etablissement)
        except Etudiant.DoesNotExist:
            messages.error(request, '❌ Étudiant non trouvé')
            return redirect('creer_pret')
        
        try:
            livre = Livre.objects.get(id=livre_id, disponible=True, etablissement=etablissement)
        except Livre.DoesNotExist:
            messages.error(request, '❌ Livre non disponible')
            return redirect('creer_pret')
        
        if date_retour:
            date_retour_prevue = datetime.strptime(date_retour, '%Y-%m-%d')
        else:
            date_retour_prevue = timezone.now() + timedelta(days=14)
        
        Pret.objects.create(
            etudiant=etudiant,
            livre=livre,
            date_retour_prevue=date_retour_prevue,
            statut='emprunte',
            etablissement=etablissement
        )
        
        livre.disponible = False
        livre.quantite_disponible -= 1
        livre.save()
        
        messages.success(request, f'✅ {etudiant.nom} {etudiant.prenom} a emprunté "{livre.titre}"')
        return redirect('accueil')
    
    livres = Livre.objects.filter(disponible=True, etablissement=etablissement) if etablissement else Livre.objects.filter(disponible=True)
    return render(request, 'livres/creer_pret.html', {'livres': livres})

@login_required
def non_rendus(request):
    etablissement = get_user_etablissement(request)
    maintenant = timezone.now().date()
    
    if request.user.is_superuser:
        prets = Pret.objects.filter(statut='emprunte').select_related('etudiant', 'livre')
    else:
        prets = Pret.objects.filter(statut='emprunte', etablissement=etablissement).select_related('etudiant', 'livre')
    
    prets_retard = []
    prets_delais = []
    
    for pret in prets:
        if pret.date_retour_prevue and pret.date_retour_prevue.date() < maintenant:
            prets_retard.append(pret)
        else:
            prets_delais.append(pret)
    
    return render(request, 'livres/non_rendus.html', {
        'prets_retard': prets_retard,
        'prets_delais': prets_delais,
    })

@login_required
def historique(request):
    etablissement = get_user_etablissement(request)
    
    # Filtrer les prêts rendus par établissement
    if request.user.is_superuser:
        prets = Pret.objects.filter(statut='rendu').select_related('etudiant', 'livre').order_by('-date_retour_reelle')
        # Pour les graphiques, super admin voit tout
        livres_populaires_all = Livre.objects.annotate(nb_emprunts=Count('pret')).filter(nb_emprunts__gt=0).order_by('-nb_emprunts')[:5]
        top_etudiants_all = Etudiant.objects.annotate(nb_emprunts=Count('pret')).filter(nb_emprunts__gt=0).order_by('-nb_emprunts')[:5]
    else:
        prets = Pret.objects.filter(statut='rendu', etablissement=etablissement).select_related('etudiant', 'livre').order_by('-date_retour_reelle')
        livres_populaires_all = Livre.objects.filter(etablissement=etablissement).annotate(nb_emprunts=Count('pret')).filter(nb_emprunts__gt=0).order_by('-nb_emprunts')[:5]
        top_etudiants_all = Etudiant.objects.filter(etablissement=etablissement).annotate(nb_emprunts=Count('pret')).filter(nb_emprunts__gt=0).order_by('-nb_emprunts')[:5]
    
    # Statistiques globales (filtrées par établissement)
    total_rendus = prets.count()
    total_emprunts = Pret.objects.filter(etablissement=etablissement).count() if not request.user.is_superuser else Pret.objects.count()
    nb_etudiants_actifs = Etudiant.objects.filter(pret__isnull=False, etablissement=etablissement).distinct().count() if not request.user.is_superuser else Etudiant.objects.filter(pret__isnull=False).distinct().count()
    
    # Top 5 livres les plus empruntés (filtrés par établissement)
    top_livres = livres_populaires_all
    top_livres_labels = [l.titre[:25] for l in top_livres]
    top_livres_data = [l.nb_emprunts for l in top_livres]
    
    # Top 5 étudiants les plus actifs (filtrés par établissement)
    top_etudiants = top_etudiants_all
    
    # Prêts par faculté (filtrés par établissement)
    faculte_noms = {
        'GL': 'Génie Logiciel', 'IIA': 'Informatique et IA', 'RSD': 'Réseaux',
        'MF': 'Management', 'MKG': 'Marketing', 'RH': 'Ressources Humaines',
        'LOG': 'Logistique', 'CG': 'Comptabilité', 'ECM': 'Économie',
        'JUR': 'Droit', 'COMM': 'Communication', 'ENT': 'Entrepreneuriat',
    }
    
    faculte_counts = {}
    for pret in prets:
        fac_code = pret.etudiant.faculte if pret.etudiant.faculte else 'Autre'
        fac_display = faculte_noms.get(fac_code, fac_code)
        faculte_counts[fac_display] = faculte_counts.get(fac_display, 0) + 1
    
    faculte_labels = list(faculte_counts.keys())
    faculte_data = list(faculte_counts.values())
    
    # Si aucune donnée, afficher un message
    if not faculte_labels:
        faculte_labels = ['Aucune donnée']
        faculte_data = [1]
    
    # Évolution des retours par mois (filtrée par établissement)
    evolution_labels = []
    evolution_data = []
    mois_francais = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    
    for i in range(5, -1, -1):
        date = timezone.now().date() - timedelta(days=30*i)
        evolution_labels.append(mois_francais[date.month - 1])
        count = prets.filter(date_retour_reelle__year=date.year, date_retour_reelle__month=date.month).count()
        evolution_data.append(count)
    
    return render(request, 'livres/historique.html', {
        'prets': prets,
        'total_rendus': total_rendus,
        'total_emprunts': total_emprunts,
        'nb_etudiants_actifs': nb_etudiants_actifs,
        'top_livres': top_livres,
        'top_livres_labels': top_livres_labels,
        'top_livres_data': top_livres_data,
        'top_etudiants': top_etudiants,
        'faculte_labels': faculte_labels,
        'faculte_data': faculte_data,
        'evolution_labels': evolution_labels,
        'evolution_data': evolution_data,
    })
@login_required
def retourner(request, pret_id):
    pret = get_object_or_404(Pret, id=pret_id)
    pret.statut = 'rendu'
    pret.date_retour_reelle = timezone.now()
    pret.save()
    
    livre = pret.livre
    livre.disponible = True
    livre.quantite_disponible += 1
    livre.save()
    
    messages.success(request, f'✅ Livre "{livre.titre}" retourné')
    return redirect('non_rendus')

@login_required
def recherche_livres(request):
    query = request.GET.get('q', '')
    categorie_id = request.GET.get('categorie', '')
    auteur = request.GET.get('auteur', '')
    disponible = request.GET.get('disponible', '')
    
    livres = Livre.objects.all()
    
    if query:
        livres = livres.filter(
            Q(titre__icontains=query) |
            Q(auteur__icontains=query) |
            Q(isbn__icontains=query)
        )
    if auteur:
        livres = livres.filter(auteur__icontains=auteur)
    if categorie_id:
        livres = livres.filter(categorie_id=categorie_id)
    if disponible == 'oui':
        livres = livres.filter(disponible=True)
    elif disponible == 'non':
        livres = livres.filter(disponible=False)
    
    categories = CategorieLivre.objects.all()
    
    return render(request, 'livres/recherche.html', {
        'livres': livres,
        'query': query,
        'categories': categories,
        'categorie_selected': categorie_id,
        'auteur': auteur,
        'disponible_selected': disponible,
    })

@login_required
def livres_par_categorie(request, categorie_id):
    categorie = get_object_or_404(CategorieLivre, id=categorie_id)
    livres = Livre.objects.filter(categorie=categorie)
    
    return render(request, 'livres/categorie_detail.html', {
        'categorie': categorie,
        'livres': livres,
        'total': livres.count(),
        'disponibles': livres.filter(disponible=True).count(),
    })