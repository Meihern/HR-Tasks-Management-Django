from Authentification.models import Employe
from .models import AccessibiliteFicheObjectif, FicheObjectif


# ACCESSIBILITE FICHE OBJECTIFS

def get_accessibilite_permission_object():
    return AccessibiliteFicheObjectif.objects.safe_get(id=1)


def get_accessibilite_remplir():
    if get_accessibilite_permission_object() is None:
        return False
    else:    
        return get_accessibilite_permission_object().fiche_evalutation_accessible


def get_accessibilite_evaluation_mi_annuelle():
    if get_accessibilite_permission_object() is None:
        return False
    else:    
        return get_accessibilite_permission_object().evaluation_mi_annuelle_accessible


def get_accessibilite_evaluation_annuelle():
    if get_accessibilite_permission_object() is None:
        return False
    else:    
        return get_accessibilite_permission_object().evaluation_annuelle_accessible


def can_add_fiche_objectif(employe: Employe):
    fiches = FicheObjectif.objects.filter(employe=employe).values('id')
    for fiche in fiches:
        if FicheObjectif.objects.get(id=fiche['id']).is_current:
            return False
    return True
