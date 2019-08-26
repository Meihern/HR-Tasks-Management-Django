from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from Authentification.models import Employe
from Authentification.manager import CustomModelManager


# Create your models here.


class FicheObjectif(models.Model):
    employe = models.ForeignKey(to=Employe, null=False, blank=False, on_delete=None, verbose_name='Employé')
    date_envoi = models.DateField(null=False, blank=False, default=now)
    bonus = models.FloatField(null=True, blank=True, verbose_name='Bonus')
    commentaire_manager = models.TextField(null=True, blank=True,
                                           verbose_name='Commentaire du Manager Performance Annuelle')
    commentaire_employe = models.TextField(null=True, blank=True,
                                           verbose_name='Commentaire Employé Performance Annuelle')
    date_validation_manager = models.DateField(null=True, blank=True, verbose_name='Date Validation Manager Annuelle')
    date_validation_employe = models.DateField(null=True, blank=True, verbose_name='Date Validation Employé Annuelle')

    objects = CustomModelManager()

    def __str__(self):
        return "Fiche des objectifs de %s" % (self.employe.get_full_name())

    def get_bonus(self):
        if self.bonus is None:
            return 0
        else:
            return self.bonus

    def get_employe(self):
        return self.employe

    def get_objectifs(self):
        objectifs = Objectif.objects.filter(fiche_objectif=self).order_by('id').values()
        return objectifs

    def get_commentaire_employe(self):
        return self.commentaire_employe

    def get_commentaire_manager(self):
        return self.commentaire_manager

    def get_date_validation_employe(self):
        return self.date_validation_employe

    def get_date_validation_manager(self):
        return self.date_validation_manager

    @property
    def is_current(self):
        if self.date_envoi.year == now().date().year:
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = 'Les fiches des objectifs'
        verbose_name = 'Fiche des objectifs'


class Objectif(models.Model):
    NOTATION_CHOICES = ((1.25, 'HP+'), (1.2, 'HP='), (1.15, 'HP-'),
                        (1.1, 'EP+'), (1.05, 'EP='), (1.03, 'EP-'),
                        (1, 'BP+'), (0.95, 'BP='), (0.85, 'BP-'),
                        (0.75, 'MP+'), (0.5, 'MP'), (0, 'FP'),
                        )

    description = models.TextField(null=False, blank=False, verbose_name="Description")
    fiche_objectif = models.ForeignKey(to=FicheObjectif, null=False, blank=False,
                                       on_delete=models.CASCADE, verbose_name="Fiche d'objectif associée")
    poids = models.FloatField(null=False, blank=False, verbose_name='Poids')
    notation_manager = models.FloatField(null=True, blank=True, verbose_name='Notation Manager',
                                         choices=NOTATION_CHOICES)
    evaluation_mi_annuelle = models.TextField(null=True, blank=True, verbose_name="Evalutation Mi-Annuelle")
    evaluation_annuelle = models.TextField(null=True, blank=True, verbose_name="Evalutation Annuelle")
    objects = CustomModelManager()

    def get_sous_objectifs(self):
        sous_objectifs = SousObjectif.objects.filter(objectif=self).order_by('id').values()
        return sous_objectifs

    def __str__(self):
        return str(self.fiche_objectif) + '\n' + 'Objectif : ' + self.description

    def get_description(self):
        return self.description

    def get_fiche_objectif_associe(self):
        return self.fiche_objectif

    def get_poids(self):
        return self.poids

    def get_notation_manager(self):
        return self.notation_manager

    def get_evaluation_mi_annuelle(self):
        return self.evaluation_mi_annuelle

    def get_evaluation_annuelle(self):
        return self.evaluation_annuelle

    def set_evaluation_mi_annuelle(self, evaluation):
        self.evaluation_mi_annuelle = evaluation

    def set_evaluation_annuelle(self, evaluation):
        self.evaluation_annuelle = evaluation

    def set_notation_manager(self, notation):
        self.notation_manager = notation

    class Meta:
        verbose_name = 'Objectif'
        verbose_name_plural = 'Objectifs'


class SousObjectif(models.Model):
    description = models.TextField(null=False, blank=False, verbose_name='Description')
    objectif = models.ForeignKey(to=Objectif, blank=False, null=False, verbose_name='Objectif_Associé',
                                 on_delete=models.CASCADE)

    objects = CustomModelManager()

    def __str__(self):
        return self.description

    def get_objectif_associe(self):
        return self.objectif

    def get_description(self):
        return self.description

    class Meta:
        verbose_name = 'Sous Objectif'
        verbose_name_plural = 'Sous Objectifs'


class AccessibiliteFicheObjectif(models.Model):
    MOIS_CHOICES = ((1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'),
                    (7, 'Juillet'), (8, 'Août'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
                    )

    mois_accessibilite_remplir_fiche = models.IntegerField(null=True, blank=True, choices=MOIS_CHOICES,
                                                           verbose_name="Mois d'accessibilité pour remplir les fiches "
                                                                        "d'objectifs")
    mois_accessibilite_evaluation_mi_annuelle = models.IntegerField(null=True, blank=True, choices=MOIS_CHOICES,
                                                                    verbose_name="Mois d'accessibilité pour "
                                                                                 "évaluation mi-annuelle des "
                                                                                 " fiches d'objectifs")
    mois_accessibilite_evaluation_annuelle = models.IntegerField(null=True, blank=True, choices=MOIS_CHOICES,
                                                                 verbose_name="Mois d'accessibilité pour "
                                                                              "évaluation Annuelle des "
                                                                              " fiches d'objectifs"
                                                                 )

    remplir_exceptionnelle_is_accessible = models.BooleanField(null=False, blank=False, default=False,
                                                               verbose_name="Etat exceptionnel d'accessibilité pour "
                                                                            "remplir les "
                                                                            "fiche des objectifs")

    evaluation_mi_annee_exceptionnelle_is_accessible = models.BooleanField(null=False, blank=False, default=False,
                                                                           verbose_name="Etat exceptionnel "
                                                                                        "d'accessibilité pour "
                                                                                        "evaluation mi-annuelle des "
                                                                                        "fiche d'objectifs")

    evaluation_annee_exceptionnelle_is_accessible = models.BooleanField(null=False, blank=False, default=False,
                                                                        verbose_name="Etat exceptionnel "
                                                                                     "d'accessibilité pour "
                                                                                     "evaluation annuelle des "
                                                                                     "fiche d'objectifs")

    objects = CustomModelManager()

    @property
    def fiche_evalutation_accessible(self):
        if self is None:
            return False
        if self.remplir_exceptionnelle_is_accessible:
            return True
        if self.mois_accessibilite_remplir_fiche:
            if self.mois_accessibilite_remplir_fiche == now().month:
                return True
            else:
                return False
        else:
            return False

    @property
    def evaluation_mi_annuelle_accessible(self):
        if self is None:
            return False
        if self.evaluation_mi_annee_exceptionnelle_is_accessible:
            return True
        if self.mois_accessibilite_evaluation_mi_annuelle:
            if self.mois_accessibilite_evaluation_mi_annuelle == now().month:
                return True
            else:
                return False
        else:
            return False

    @property
    def evaluation_annuelle_accessible(self):
        if self is None:
            return False
        if self.evaluation_annee_exceptionnelle_is_accessible:
            return True
        if self.mois_accessibilite_evaluation_annuelle:
            if self.mois_accessibilite_evaluation_annuelle == now().month:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        message = ""
        if self.fiche_evalutation_accessible:
            message += "Remplir les fiches des objectifs est accessible \n"
        else:
            message += "Remplir les fiches des objectifs est inaccessible \n"
        if self.evaluation_mi_annuelle_accessible:
            message += "Evaluation Mi-Annuelle est accessible \n"
        else:
            message += "Evaluation Mi-Annuelle est inaccessible \n"
        if self.evaluation_annuelle_accessible:
            message += "Evaluation Annuelle est accessible \n"
        else:
            message += "Evaluation Annuelle est inaccessible \n"
        return message

    def save(self, *args, **kwargs):
        if AccessibiliteFicheObjectif.objects.exists() and not self.pk:
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError("Une seule permission d'accessibilité est possible")
        return super(AccessibiliteFicheObjectif, self).save(*args, **kwargs)


    class Meta:
        verbose_name = "Permission d'accesibilité aux fonctionnalités Fiche Objectif"
        verbose_name_plural = "Permissions d'accesibilité aux fonctionnalités Fiche Objectif"

