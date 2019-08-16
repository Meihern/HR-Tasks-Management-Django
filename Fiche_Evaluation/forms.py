from django import forms


class FicheObjectifForm(forms.Form):
    FIELD_NAME_MAPPING = {
        'objectif': 'objectif[]',
        'poids': 'poids[]',
        'sous_objectif': 'sous_objectif[]',
    }

    objectif = forms.CharField(max_length=255, required=True, widget=forms.TextInput)
    poids = forms.DecimalField(min_value=0.1, max_value=1, max_digits=3,
                               decimal_places=2, required=True, widget=forms.NumberInput)
    sous_objectif = forms.CharField(max_length=255, required=True, widget=forms.TextInput)
