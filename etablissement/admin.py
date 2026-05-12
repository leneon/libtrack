from django.contrib import admin
from .models import Etablissement

@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'telephone')
    search_fields = ('nom', 'code')
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_view_permission(self, request, obj=None):
        return True