from django.contrib import admin
from django.shortcuts import redirect
from django import forms
from .models import Etudiant, Faculte

# ========== FACULTE ==========
@admin.register(Faculte)
class FaculteAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

# ========== ETUDIANTS ==========
class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = kwargs.get('request')
        if request and hasattr(request, 'user'):
            try:
                etablissement = request.user.profile.etablissement
                self.fields['etablissement'].initial = etablissement
                self.fields['etablissement'].widget = forms.HiddenInput()
            except:
                pass

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    form = EtudiantForm
    list_display = ('nom', 'prenom', 'classe', 'faculte', 'carte_id', 'telephone')
    list_filter = ('faculte',)
    search_fields = ('nom', 'prenom', 'carte_id', 'classe')
    
    # AUTOCOMPLETION POUR FACULTE
    autocomplete_fields = ('faculte',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form
    
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/')