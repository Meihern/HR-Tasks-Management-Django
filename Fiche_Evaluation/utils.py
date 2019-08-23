from django.utils.timezone import now


def fiche_evalutation_accessible():
    if now().date().month != 1:
        return False
    else:
        return True


def evaluation_mi_annuelle_accessible():
    if now().date().month != 8:
        return False
    else:
        return True


def evaluation_annuelle_accessible():
    if now().date().month != 8:
        return False
    else:
        return True


def get_percentage_value(value: float):
    if value is None:
        return 0
    else:
        return int(value*100)


def get_resultat_evaluation(value: float):
    pass