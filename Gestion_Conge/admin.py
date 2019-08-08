from django.contrib import admin
from .models import DemandeConge
# Register your models here.


class DemandeCongeAdmin(admin.ModelAdmin):

    list_display = ('etat', 'employe', 'date_envoi', 'date_depart', 'date_retour')
    list_filter = ('etat',)
    search_fields = ('employe__full_name',)


admin.site.register(DemandeConge, DemandeCongeAdmin)