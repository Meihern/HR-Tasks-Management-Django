from django import forms
from django.forms.utils import ErrorList
from Fiche_Evaluation.models import Objectif

def clean_poids(poids: list):
    for i in range(len(poids)):
        poids[i] = int(poids[i])
    return poids


class FicheObjectifForm(forms.Form):
    FIELD_NAME_MAPPING = {
        'objectif': 'objectifs[]',
        'poids': 'poids[]',
        'sous_objectif': 'sous_objectifs_objectif_id[]',
    }

    objectif = forms.CharField(max_length=255,  widget=forms.TextInput, required=False)
    poids = forms.IntegerField(min_value=10, max_value=100, widget=forms.NumberInput, required=False)
    sous_objectif = forms.CharField(max_length=255, widget=forms.TextInput, required=False)

    def is_valid_poids(self, poids):
        if not poids:
            self.errors['poids'] = ErrorList()
            self.errors['poids'].append("Vous devez définir au moins un seul poids valide")
            return False
        clean_poids(poids)
        for i in range(len(poids)):
            if not 10 <= poids[i] <= 100:
                self.errors['poids'] = ErrorList()
                self.errors['poids'].append("La valeur du poids doit être comprise entre 10 et 100")
                return False

        if sum(poids) != 100:
            self.errors['poids'] = ErrorList()
            self.errors['poids'].append("La valeur totale des poids doit être égale à 100")
            return False

        return True

    def is_valid_objectifs(self, objectifs: list):
        if not objectifs:
            self.errors['objectif'] = ErrorList()
            self.errors['objectif'].append("Vous devez définir au moins un seul objectif")
        else:
            return True

    def is_valid(self, objectifs: list, poids: list, sous_objectifs: list=None):
        is_valid = super(FicheObjectifForm, self).is_valid()
        if self.is_valid_objectifs(objectifs) and self.is_valid_poids(poids) and is_valid:
            return True
        else:
            return False


class EvaluationMiAnnuelleForm(forms.Form):

    evaluation_mi_annuelle = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Objectif
        fields = ('evaluation_mi_annuelle',)


class EvaluationAnnuelleForm(forms.Form):

    evaluation_annuelle = forms.CharField(required=False, widget=forms.Textarea)
    notation_manager = forms.ChoiceField(choices=Objectif.NOTATION_CHOICES, required=True, widget=forms.Select)

    class Meta:
        model = Objectif
        fields = ('evaluation_annuelle', 'notation_manager')


