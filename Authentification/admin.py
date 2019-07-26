# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from .forms import EmployeAdminCreationForm, EmployeAdminChangeForm
from .models import Employe,Departement



def make_employe_active(modeladmin,request,queryset):
    queryset.update(active=True)
make_employe_active.short_description = "Rendre les comptes sélectionnés actifs"

def make_employe_inactive(modeladmin,request,queryset):
    queryset.update(active=False)
make_employe_inactive.short_description = "Rendre les comptes sélectionnés inactifs"


class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    #form = EmployeAdminChangeForm
    #add_form = EmployeAdminChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','last_name','first_name','fonction','department', 'admin','active','staff')
    list_filter = ('admin', 'staff', 'active','sexe','department')

    fieldsets = (
        (None, {'fields': ('last_name', 'first_name', 'email', 'password', 'matricule_paie', 'n_cin', 'n_cnss', 'fonction','date_naissance','last_login','superieur_hierarchique')}),
        # ('Full name', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'n_cin', 'matricule_paie')}
         ),
    )
    search_fields = ('email', 'last_name', 'first_name', 'n_cin', 'matricule_paie', 'fonction', 'ville')
    ordering = ('email',)
    filter_horizontal = ()
    actions = [make_employe_active,make_employe_inactive]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('nom_departement','directeur')
    list_filter = ('nom_departement',)
    search_fields = ('nom_departement',)


admin.site.register(Employe, CustomUserAdmin)
admin.site.register(Departement,DepartmentAdmin)
admin.site.unregister(Group)
