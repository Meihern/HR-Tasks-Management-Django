from django.contrib.auth.models import AnonymousUser

from Fiche_Evaluation.permissions import *


def fiche_evaluation_permissions_processor(request):
    is_fiche_accessible = get_accessibilite_remplir()
    is_evaluation_annuelle_accessible = get_accessibilite_evaluation_annuelle()
    is_evaluation_mi_annuelle_accessible = get_accessibilite_evaluation_mi_annuelle()
    if request.user is not None and not request.user.is_anonymous:
        if can_add_fiche_objectif(request.user):
            can_add_fiche = True
        else:
            can_add_fiche = False

        print(is_fiche_accessible, is_evaluation_annuelle_accessible, is_evaluation_mi_annuelle_accessible, can_add_fiche)
        return {'is_fiche_accessible': is_fiche_accessible,
                'is_evaluation_annuelle_accessible': is_evaluation_annuelle_accessible,
                'is_evaluation_mi_annuelle_accessible': is_evaluation_mi_annuelle_accessible,
                'can_add_fiche': can_add_fiche}
    else:
        print(is_fiche_accessible, is_evaluation_annuelle_accessible, is_evaluation_mi_annuelle_accessible)
        return {'is_fiche_accessible': is_fiche_accessible,
                'is_evaluation_annuelle_accessible': is_evaluation_annuelle_accessible,
                'is_evaluation_mi_annuelle_accessible': is_evaluation_mi_annuelle_accessible
                }
