from django.contrib import admin
from django.shortcuts import redirect
from django import forms
from django.db.models import Q
from .models import CategorieLivre, Livre, Pret
from etudiants.models import Etudiant
from etablissement.models import Etablissement

# ========== CATEGORIE LIVRES ==========
@admin.register(CategorieLivre)
class CategorieLivreAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

# ========== LIVRES ==========
class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = kwargs.get('request')
        if request and hasattr(request, 'user'):
            try:
                etablissement = request.user.profile.etablissement
                self.fields['etablissement'].initial = etablissement
                self.fields['etablissement'].widget = forms.HiddenInput()
                # Filtrer les catégories par établissement
                self.fields['categorie'].queryset = CategorieLivre.objects.filter(etablissement=etablissement)
            except:
                pass

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    form = LivreForm
    list_display = ('numero_livre', 'titre', 'auteur', 'categorie', 'disponible')
    list_filter = ('categorie', 'disponible')
    search_fields = ('titre', 'auteur', 'numero_livre')
    
    # AUTOCOMPLETION POUR LA CATEGORIE
    autocomplete_fields = ('categorie',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form
    
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/')

# ========== PRETS ==========
class PretForm(forms.ModelForm):
    class Meta:
        model = Pret
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = kwargs.get('request')
        if request and hasattr(request, 'user'):
            try:
                etablissement = request.user.profile.etablissement
                # Filtrer par établissement
                self.fields['livre'].queryset = Livre.objects.filter(etablissement=etablissement)
                self.fields['etudiant'].queryset = Etudiant.objects.filter(etablissement=etablissement)
                self.fields['etablissement'].initial = etablissement
                self.fields['etablissement'].widget = forms.HiddenInput()
            except:
                pass

@admin.register(Pret)
class PretAdmin(admin.ModelAdmin):
    form = PretForm
    list_display = ('etudiant', 'livre', 'statut', 'date_emprunt', 'date_retour_prevue')
    list_filter = ('statut',)
    search_fields = ('etudiant__nom', 'etudiant__prenom', 'etudiant__carte_id', 'livre__titre')
    
    # AUTOCOMPLETION POUR ETUDIANT ET LIVRE
    autocomplete_fields = ('etudiant', 'livre')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form
    
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/')