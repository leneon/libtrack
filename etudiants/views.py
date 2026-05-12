from django.shortcuts import render
from .models import Etudiant

def liste_etudiants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'etudiants/liste.html', {'etudiants': etudiants})