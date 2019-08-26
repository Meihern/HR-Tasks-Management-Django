from django.contrib import admin
from .models import *


# Register your models here.


class FicheObjectifAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_envoi', 'bonus')

    def has_add_permission(self, request):
        return False


class ObjectifAdmin(admin.ModelAdmin):
    list_display = ('fiche_objectif', 'description', 'poids', 'notation_manager')

    def has_add_permission(self, request):
        return False


class SousObjectifAdmin(admin.ModelAdmin):
    list_display = ('objectif', 'description')

    def has_add_permission(self, request):
        return False


class AccessbiliteFicheObjectifAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if AccessibiliteFicheObjectif.objects.exists():
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_or_change_permission(self, request, obj=None):
        return True


admin.site.register(FicheObjectif, FicheObjectifAdmin)
admin.site.register(Objectif, ObjectifAdmin)
admin.site.register(SousObjectif, SousObjectifAdmin)
admin.site.register(AccessibiliteFicheObjectif, AccessbiliteFicheObjectifAdmin)
