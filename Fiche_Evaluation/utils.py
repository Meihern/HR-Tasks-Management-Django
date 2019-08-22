from django.utils.timezone import now


def fiche_evalutation_accessible():
    if now().date().month != 1:
        return False
    else:
        return True


def evaluation_mi_annuelle_accessible():
    if now().date().month != 6:
        return False
    else:
        return True


def evaluation_annuelle_accessible():
    if now().date().month != 12:
        return False
    else:
        return True