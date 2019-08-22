from django.contrib import admin
from .models import *
# Register your models here.


class FicheObjectifAdmin(admin.ModelAdmin):

    list_display = ('employe', 'date_envoi', 'bonus')


class ObjectifAdmin(admin.ModelAdmin):

    list_display = ('fiche_objectif', 'description', 'poids', 'notation_manager')


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('objectif', 'description')


class SousObjectifAdmin(admin.ModelAdmin):
    list_display = ('objectif', 'description')


admin.site.register(FicheObjectif, FicheObjectifAdmin)
admin.site.register(Objectif, ObjectifAdmin)
admin.site.register(SousObjectif, SousObjectifAdmin)
