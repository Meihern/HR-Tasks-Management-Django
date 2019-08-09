from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import DemandeConge
from django.utils.timezone import now
from django.forms.utils import ErrorList


class DemandeCongeForm(forms.ModelForm):

    date_depart = forms.DateField(required=True, widget=forms.DateInput)
    date_retour = forms.DateField(required=True, widget=forms.DateInput)
    jours_ouvrables = forms.IntegerField(min_value=0, max_value=20, required=True, widget=forms.NumberInput)
    interim = forms.CharField(widget=forms.TextInput, required=False)
    telephone = PhoneNumberField(required=False)

    def valid_date(self):
        self._errors['date_depart'] = ErrorList()
        self._errors['date_retour'] = ErrorList()
        if self.cleaned_data['date_depart'] < now().date():
            self.errors['date_depart'].append("La date de départ doit être supérieure à la date d'ajourd'hui")
            return False
        if self.cleaned_data['date_retour'] < now().date():
            self.errors['date_retour'].append("La date de retour doit être supérieure à la date d'ajourd'hui")
        elif self.cleaned_data['date_depart'] >= self.cleaned_data['date_retour']:
            self._errors['date_depart'].append('La date de départ doit être inférieure à la date de retour')
            self._errors['date_retour'].append('La date de retour doit être supérieure à la date de départ')
            return False
        else:
            return True

    def is_valid(self):
        valid = super(DemandeCongeForm, self).is_valid()
        valid_date = self.valid_date()

        if valid and valid_date:
            return True
        else:
            return False

    class Meta:
        model = DemandeConge
        fields = ('date_depart', 'date_retour', 'jours_ouvrables', 'interim', 'telephone')