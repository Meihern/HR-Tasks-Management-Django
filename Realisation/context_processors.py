from Fiche_Evaluation.permissions import *


def fiche_evaluation_permissions_processor(request):
    is_fiche_accessible = get_accessibilite_remplir()
    is_evaluation_annuelle_accessible = get_accessibilite_evaluation_annuelle()
    is_evaluation_mi_annuelle_accessible = get_accessibilite_evaluation_mi_annuelle()
    return {'is_fiche_accessible': is_fiche_accessible,
            'is_evaluation_annuelle_accessible': is_evaluation_annuelle_accessible,
            'is_evaluation_mi_annuelle_accessible': is_evaluation_mi_annuelle_accessible}