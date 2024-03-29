# users/admin.py
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from django.core.mail import send_mail
from django.template import loader
from Notifications.models import Notification
from Realisation.settings import DEFAULT_FROM_EMAIL
from .models import Departement, Service, Activite, Agence, CostCenter
from .ressources import EmployeResource, ServiceResource, CostCenterResource, AgenceResource, \
    DepartmentResource, ActiviteResource

Employe = get_user_model()


def make_employe_active(modeladmin, request, queryset):
    queryset.update(active=True)


make_employe_active.short_description = "Rendre les comptes sélectionnés actifs"


def make_employe_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


make_employe_inactive.short_description = "Rendre les comptes sélectionnés inactifs"


def notify_employe_to_fill_fiche_objectif(modeladmin, request, queryset):
    context = {
        'site_name': 'EMID Digitalisation Services RH',
        'protocol': 'http',
        'domain': request.META['HTTP_HOST']
    }
    for employe in queryset:
        context['employe'] = employe
        email = loader.render_to_string("Fiche_evaluation/email_rappel_fiche_objectif.html", context)
        notification = Notification(no_reply=True, receiver=employe, sender=request.user, subject='Rappel',
                                    message='Veuillez remplir votre Fiche des Objectifs')
        notification.save()
        if employe.email:
            send_mail(subject='Rappel Fiche Objectifs', fail_silently=True, from_email=DEFAULT_FROM_EMAIL,
                      recipient_list=[employe.get_email()], message=email)
    messages.success(request, 'Employés notifiés avec succès')


notify_employe_to_fill_fiche_objectif.short_description = "Notifier les employés sélectionnés pour remplir leurs fiches d'objectifs"


class CustomUserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    # The forms to add and change user instances
    # form = EmployeAdminChangeForm
    # add_form = EmployeAdminCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'full_name', 'fonction', 'department', 'superieur_hierarchique', 'activite', 'admin', 'active', 'staff')
    list_filter = (
        'admin', 'staff', 'active', 'sexe', 'department', 'activite', 'consultant_fiches_objectifs',
        'consultant_attestations',
        'consultant_conges')

    fieldsets = (
        (
            None,
            {'fields': ('full_name', 'matricule_paie', 'password', 'email', 'n_cin', 'n_cnss', 'n_compte', 'fonction',
                        'date_naissance', 'last_login', 'superieur_hierarchique', 'department', 'activite', 'ville',
                        'agence')}),
        # ('Full name', {'fields': ()}),
        ('Permissions', {'fields': ('staff', 'admin', 'active', 'consultant_fiches_objectifs',
                                    'consultant_attestations', 'consultant_conges')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matricule_paie', 'password1', 'password2')}
         ),
    )

    search_fields = ('email', 'full_name', 'matricule_paie', 'fonction', 'ville')
    ordering = ('email', 'matricule_paie')
    filter_horizontal = ()
    actions = [make_employe_active, make_employe_inactive, notify_employe_to_fill_fiche_objectif]
    resource_class = EmployeResource


class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('nom_departement', 'directeur')
    list_filter = ('nom_departement',)
    search_fields = ('nom_departement',)
    resource_class = DepartmentResource


class ActiviteAdmin(ImportExportModelAdmin):
    list_display = ('nom_activite',)
    list_filter = ('nom_activite',)
    search_fields = ('nom_activite',)
    reource_class = ActiviteResource


class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('nom_service',)
    list_filter = ('nom_service',)
    search_fields = ('nom_service',)
    resource_class = ServiceResource


class AgenceAdmin(ImportExportModelAdmin):
    list_display = ('nom_agence',)
    list_filter = ('nom_agence',)
    search_fields = ('nom_agence',)
    resource_class = AgenceResource


class CostCenterAdmin(ImportExportModelAdmin):
    list_display = ('nom_cost_center',)
    list_filter = ('nom_cost_center',)
    search_fields = ('nom_cost_center',)
    resource_class = CostCenterResource


admin.site.register(Employe, CustomUserAdmin)
admin.site.register(Departement, DepartmentAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Activite, ActiviteAdmin)
admin.site.register(Agence, AgenceAdmin)
admin.site.register(CostCenter, CostCenterAdmin)
admin.site.unregister(Group)
