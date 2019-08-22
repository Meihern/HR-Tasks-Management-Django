from django.utils.timezone import now


def fiche_evalutation_accessible():
    if now().date().month != 1:
        return False
    else:
        return True
