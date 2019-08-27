from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from Gestion_Attestations.ressources import SalaireResource
from .models import DemandeAttestation, TypeDemandeAttestation, Salaire


# Register your models here.


class DemandeAttestationAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type', 'date_envoi', 'etat_validation')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SalaireAdmin(ImportExportModelAdmin):
    list_display = ('valeur_brute', 'matricule_paie')
    search_fields = ('matricule_paie__full_name',)
    resource_class = SalaireResource


class TypeDemandeAttestationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if TypeDemandeAttestation.objects.safe_get(nom_type_demande='salaire') and TypeDemandeAttestation.objects.safe_get(nom_type_demande='travail') and TypeDemandeAttestation.objects.safe_get(nom_type_demande='domiciliation'):
            return False
        else:
            return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(TypeDemandeAttestation, TypeDemandeAttestationAdmin)
admin.site.register(DemandeAttestation, DemandeAttestationAdmin)
admin.site.register(Salaire, SalaireAdmin)
