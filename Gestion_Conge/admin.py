from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from Gestion_Conge.ressources import SoldeCongeResource
from .models import DemandeConge, SoldeConge


# Register your models here.


class DemandeCongeAdmin(admin.ModelAdmin):
    list_display = ('etat', 'employe', 'date_envoi', 'date_depart', 'date_retour')
    list_filter = ('etat',)
    search_fields = ('employe__full_name',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class SoldeCongeAdmin(ImportExportModelAdmin):
    list_display = ('solde', 'matricule_paie')
    search_fields = ('matricule_paie__full_name',)
    resource_class = SoldeCongeResource


admin.site.register(DemandeConge, DemandeCongeAdmin)
admin.site.register(SoldeConge, SoldeCongeAdmin)
