from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from Gestion_Attestations.ressources import SalaireResource
from .models import DemandeAttestation, TypeDemandeAttestation, Salaire


# Register your models here.


class DemandeAttestationAdmin(admin.ModelAdmin):
    list_display = ('employe','type','date_envoi','etat_validation')


class SalaireAdmin(ImportExportModelAdmin):
    list_display = ('valeur_brute', 'matricule_paie')
    search_fields = ('matricule_paie__full_name',)
    resource_class = SalaireResource


admin.site.register(TypeDemandeAttestation)
admin.site.register(DemandeAttestation,DemandeAttestationAdmin)
admin.site.register(Salaire, SalaireAdmin)
