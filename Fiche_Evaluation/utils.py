from Authentification.models import Employe
from Fiche_Evaluation.models import FicheObjectif, Objectif, SousObjectif


def get_percentage_value(value: float):
    if value is None:
        return 0
    else:
        return int(value*100)


def load_fiche_data(fiche_objectif: FicheObjectif):
    objectifs = fiche_objectif.get_objectifs()
    data_objectifs = []
    for data in objectifs:
        objectif = Objectif.objects.get(id=data['id'])
        sous_objectifs = objectif.get_sous_objectifs()
        data_sous_objectifs = []
        for data2 in sous_objectifs:
            sous_objectif = SousObjectif.objects.get(id=data2['id'])
            sous_objectif = {
                'id_sous_objectif': sous_objectif.id,
                'description': sous_objectif.get_description()
            }
            data_sous_objectifs.append(sous_objectif)
        objectif = {
            'id_objectif': objectif.id,
            'description': objectif.get_description(),
            'sous_objectifs': data_sous_objectifs,
            'poids': get_percentage_value(objectif.get_poids()),
            'evaluation_mi_annuelle': objectif.get_evaluation_mi_annuelle() if objectif.get_evaluation_mi_annuelle() else '',
            'evaluation_annuelle': objectif.get_evaluation_annuelle() if objectif.get_evaluation_annuelle() else '',
            'notation_manager': objectif.get_notation_manager_display() if objectif.get_notation_manager_display() else '',
            'notation_manager_value': int(objectif.get_notation_manager()*100) if objectif.get_notation_manager() else 0,
        }
        data_objectifs.append(objectif)
    fiche = {
        'id': fiche_objectif.id,
        'employe': fiche_objectif.get_employe(),
        'bonus': fiche_objectif.get_bonus() if fiche_objectif.get_bonus() else '',
        'commentaire_manager': fiche_objectif.get_commentaire_manager() if fiche_objectif.get_commentaire_manager else '',
        'commentaire_employe': fiche_objectif.get_commentaire_employe() if fiche_objectif.get_commentaire_employe() else ''
    }
    return data_objectifs, fiche


def load_equipe_current_fiches(employe: Employe):
    equipe = Employe.objects.filter(superieur_hierarchique=employe)
    fiche_objectifs = FicheObjectif.objects.filter(employe__in=equipe)
    fiche_objectifs = fiche_objectifs.all().values('id')
    data = []
    for fiche in fiche_objectifs:
        fiche = FicheObjectif.objects.safe_get(id=fiche['id'])
        if fiche.is_current:
            fiche_objectif = {
                'id': fiche.id,
                'employe': fiche.get_employe().get_full_name(),
                'fonction': fiche.get_employe().get_fonction()
            }
            data.append(fiche_objectif)
    return data


def get_resultat_evaluation(value: float):
    pass