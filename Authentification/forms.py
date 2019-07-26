# users/forms.py
from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, get_user_model, ReadOnlyPasswordHashField, PasswordChangeForm
from .models import Employe

Employe = get_user_model()


class EmployeAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    numero_cin = forms.CharField(label='Numero de Cin',widget=forms.CharField)
    matricule_paie = forms.CharField(label='Matricule Paie',widget=forms.IntegerField)

    class Meta:
        model = Employe
        fields = ('email','n_cin','matricule_paie') #'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        employe = super(EmployeAdminCreationForm, self).save(commit=False)
        employe.set_password(self.cleaned_data["password1"])
        if commit:
            employe.save()
        return employe



class EmployeAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Employe
        fields = ('last_name', 'first_name', 'matricule_paie', 'n_cin', 'n_cnss','date_naissance','superieur_hierarchique', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    '''
    def confirm_login_allowed(self, employe):
        if not employe.is_active:
            raise forms.ValidationError(
                ("This account is inactive."),
                code='inactive',
            )
        return True
    '''
    class Meta:
        model = Employe
        fields = ('email', 'password')


class ChangePasswordForm(forms.Form):
    email = forms.CharField(required=True,widget=forms.HiddenInput)
    old_password = forms.CharField(required=True, widget=forms.PasswordInput)
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = Employe
        fields = ('email','password')




