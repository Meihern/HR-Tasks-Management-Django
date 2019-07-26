from django.contrib import admin
from .models import DemandeAttestation, TypeDemandeAttestataion

# Register your models here.
admin.site.register(TypeDemandeAttestataion)
admin.site.register(DemandeAttestation)
