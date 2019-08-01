from django.contrib import admin
from .models import DemandeAttestation, TypeDemandeAttestatation

# Register your models here.
class DemandeAttestationAdmin(admin.ModelAdmin):
    list_display = ('employe','type','date_envoi','etat_validation')


admin.site.register(TypeDemandeAttestatation)
admin.site.register(DemandeAttestation,DemandeAttestationAdmin)
