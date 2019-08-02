# users/forms.py
from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, get_user_model, ReadOnlyPasswordHashField, PasswordChangeForm

Employe = get_user_model()


class EmployeAdminCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    matricule_paie = forms.CharField(label='Matricule Paie', widget=forms.IntegerField)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


    class Meta:
        model = Employe
        fields = ('matricule_paie', 'password') #'full_name',)

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



class EmployeAdminChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Employe
        fields = ('full_name', 'matricule_paie', 'password', 'email', 'n_cin', 'n_cnss',
                  'n_compte', 'fonction','date_naissance','last_login','superieur_hierarchique','department')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):

    matricule_paie = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Employe
        fields = ('matricule_paie', 'password')


class ChangePasswordForm(forms.Form):
    matricule_paie = forms.CharField(required=True, widget=forms.HiddenInput)
    old_password = forms.CharField(required=True, widget=forms.PasswordInput)
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = Employe
        fields = ('matricule_paie', 'password')




