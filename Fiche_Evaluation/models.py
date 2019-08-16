from django.db import models
from django.utils.timezone import now

from Authentification.models import Employe
from Authentification.manager import CustomModelManager

# Create your models here.


def get_percentage_value(value: float):
    if value is None:
        return 0
    else:
        return value*100


def get_resultat_evaluation(value: float):
    pass


class FicheObjectif(models.Model):
    employe = models.ForeignKey(to=Employe, null=False, blank=False, on_delete=None, verbose_name='Employé')
    date_envoi = models.DateField(null=False, blank=False, default=now)
    bonus = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name='Bonus')
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
        objectifs = Objectif.objects.filter(fiche_objectif=self).values()
        return objectifs

    class Meta:
        verbose_name_plural = 'Les fiches des objectifs'
        verbose_name = 'Fiche des objectifs'


class Objectif(models.Model):
    description = models.TextField(null=False, blank=False, verbose_name="Description")
    fiche_objectif = models.ForeignKey(to=FicheObjectif, null=False, blank=False,
                                       on_delete=models.CASCADE, verbose_name="Fiche d'objectif associée")
    poids = models.DecimalField(max_digits=3, decimal_places=2, null=False, blank=False, verbose_name='Poids')
    notation_manager = models.DecimalField(max_digits=3, decimal_places=2,
                                           null=True, blank=True, verbose_name='Notation Manager')

    objects = CustomModelManager()

    def get_sous_objectifs(self):
        sous_objectifs = SousObjectif.objects.filter(objectif=self).values()
        return sous_objectifs

    def get_evaluation(self):
        evaluation = Evaluation.objects.safe_get(objectif=self)
        return evaluation

    def __str__(self):
        return str(self.fiche_objectif)+'\n'+'Objectif : '+self.description

    def get_fiche_objectif_associe(self):
        return self.fiche_objectif

    def get_poids(self):
        return self.poids

    def get_notation_manager(self):
        if self.notation_manager is None:
            return 0
        else:
            return self.notation_manager

    class Meta:
        verbose_name = 'Objectif'
        verbose_name_plural = 'Objectifs'


class Evaluation(models.Model):
    description = models.TextField(null=False, blank=False, verbose_name='Description')
    objectif = models.OneToOneField(to=Objectif, blank=False, null=False, verbose_name='Objectif Associé',
                                    on_delete=models.CASCADE)

    objects = CustomModelManager()

    def __str__(self):
        return self.description

    def get_objectif_associe(self):
        return self.objectif

    class Meta:
        verbose_name_plural = 'Evaluations'
        verbose_name = 'Evaluation'


class SousObjectif(models.Model):
    description = models.TextField(null=False, blank=False, verbose_name='Description')
    objectif = models.ForeignKey(to=Objectif, blank=False, null=False, verbose_name='Objectif_Associé', on_delete=models.CASCADE)

    objects = CustomModelManager()

    def __str__(self):
        return self.description

    def get_objectif_associe(self):
        return self.objectif

    class Meta:
        verbose_name = 'Sous Objectif'
        verbose_name_plural = 'Sous Objectifs'






