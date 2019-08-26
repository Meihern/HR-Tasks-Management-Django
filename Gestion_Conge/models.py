from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from Authentification.manager import CustomModelManager
from Authentification.models import Employe, Departement
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now


# Create your models here.


class DemandeConge(models.Model):
    # Constants

    ETAT_REFUS = 0
    ETAT_ENVOI = 1
    ETAT_SUPERIEUR_HIERARCHIQUE = 2
    ETAT_DIRECTION_CONCERNEE = 3
    ETAT_DIRECTION_RH = 4
    CHOIX_ETATS = ((ETAT_ENVOI, 'En attente de validation par le supérieur hiérachique'),
                   (ETAT_SUPERIEUR_HIERARCHIQUE, 'En attente de validation par la direction concernée'),
                   (ETAT_DIRECTION_CONCERNEE, 'En attente de validation par la direction RH'),
                   (ETAT_DIRECTION_RH, 'Demande de Congé validée'),
                   (ETAT_REFUS, 'Demande de Congé refusée'))
    # Fields

    date_depart = models.DateField(null=False, blank=False, verbose_name='Date Départ en Congé')
    date_retour = models.DateField(null=False, blank=False, verbose_name='Date Retour du Congé')
    employe = models.ForeignKey(Employe, null=False, blank=False, on_delete=None, verbose_name='Employé')
    jours_ouvrables = models.PositiveIntegerField(null=False, blank=False, verbose_name='Jours Ouvrables')
    interim = models.CharField(max_length=60, null=True, blank=True, verbose_name='Intérim assuré par')
    telephone = PhoneNumberField(null=True, blank=True, unique=False, verbose_name='Téléphone personnel')
    etat = models.PositiveSmallIntegerField(null=False, blank=False, default=ETAT_ENVOI,
                                            choices=CHOIX_ETATS, verbose_name='Etat Demande')
    date_envoi = models.DateField(null=False, blank=False, default=now,
                                  verbose_name='Date envoi de la demande du Congé')
    date_sup = models.DateField(null=True, blank=True, verbose_name='Date validation Hiérarchie')
    date_direction = models.DateField(null=True, blank=True, verbose_name='Date validation Direction Concernée')
    date_direction_rh = models.DateField(null=True, blank=True, verbose_name='Date validation direction RH')

    # Functions and Properties

    objects = CustomModelManager()
    notifications = GenericRelation('Notifications.Notification')

    def __str__(self):
        return ("%s a demandé un congé du %s au %s avec %s jours ouvrables." %
                (self.get_employe().get_full_name(),
                 self.get_date_depart(),
                 self.get_date_retour(),
                 self.get_jours_ouvrables()))

    def update_etat(self, code_etat: int):

        if code_etat == self.ETAT_SUPERIEUR_HIERARCHIQUE:
            DemandeConge.objects.filter(id=self.pk).update(etat=self.ETAT_SUPERIEUR_HIERARCHIQUE, date_sup=now())

        if code_etat == self.ETAT_DIRECTION_CONCERNEE:
            if self.date_sup:
                DemandeConge.objects.filter(id=self.pk).update(etat=self.ETAT_DIRECTION_CONCERNEE, date_direction=now())
            else:
                DemandeConge.objects.filter(id=self.pk).update(etat=self.ETAT_DIRECTION_CONCERNEE, date_direction=now(),
                                                               date_sup=now())
        if code_etat == self.ETAT_DIRECTION_RH:
            if self.date_sup and self.date_direction:
                DemandeConge.objects.filter(id=self.pk).update(etat=self.ETAT_DIRECTION_RH, date_direction_rh=now())
            elif self.date_direction:
                DemandeConge.objects.filter(id=self.pk).update(etat=self.ETAT_DIRECTION_RH, date_direction_rh=now(),
                                                               date_sup=now())
            else:
                DemandeConge.objects.filter(id=self.pk).update(etat=self.ETAT_DIRECTION_RH,
                                                               date_direction_rh=now(),
                                                               date_sup=now(), date_direction=now())

        if code_etat == self.ETAT_REFUS:
            DemandeConge.objects.filter(id=self.pk).update(etat=self.ETAT_REFUS)

    def get_id(self):
        return self.pk

    def get_employe(self):
        return self.employe

    def get_interim(self):
        if self.interim:
            return self.interim
        else:
            return None

    def get_telephone(self):
        if self.telephone:
            return self.telephone
        else:
            return None

    def get_etat(self):
        return self.etat

    def get_date_depart(self):
        return self.date_depart

    def get_date_retour(self):
        return self.date_retour

    def get_date_envoi(self):
        return self.date_envoi

    def get_date_sup(self):
        return self.date_sup

    def get_date_direction(self):
        return self.date_direction

    def get_date_direction_rh(self):
        return self.date_direction_rh

    def get_jours_ouvrables(self):
        return self.jours_ouvrables

    @property
    def in_conge(self):

        if self.get_date_depart() <= now().date() < self.get_date_retour() and self.etat == DemandeConge.ETAT_DIRECTION_RH:
            return True
        else:
            return False

    @property
    def is_upcoming_conge(self):

        if self.get_date_depart() > now().date() and self.get_etat() == DemandeConge.ETAT_DIRECTION_RH:
            return True
        else:
            return False

    class Meta:
        verbose_name = "Demande Congé"
        verbose_name_plural = "Demandes des Congés"


class SoldeConge(models.Model):
    solde = models.IntegerField(null=False, blank=False, verbose_name='Solde de Congé')
    matricule_paie = models.OneToOneField(to=Employe, null=False, blank=False, verbose_name='Employé', on_delete=models.CASCADE)

    def __str__(self):
        return "Solde de % est : %s"%(self.matricule_paie.get_full_name(), self.solde)

    class Meta:
        verbose_name = 'Solde de Congé'
        verbose_name_plural = 'Les soldes des congés'
