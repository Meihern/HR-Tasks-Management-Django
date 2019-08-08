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
    date_envoi = models.DateField(null=False, blank=False, default=now, verbose_name='Date envoi de la demande du Congé')
    date_sup = models.DateField(null=True, blank=True, verbose_name='Date validation Hiérarchie')
    date_direction = models.DateField(null=True, blank=True, verbose_name='Date validation Direction Concernée')
    date_direction_rh = models.DateField(null=True, blank=True, verbose_name='Date validation direction RH')

    # Functions and Properties

    objects = CustomModelManager()

    def __str__(self):
        return "Demande de congé envoyé par %s"%(self.employe.get_full_name())

    def update_etat(self, code_etat:int):
        if code_etat == self.ETAT_SUPERIEUR_HIERARCHIQUE:
            DemandeConge.objects.filter(id=self.pk).update(etat=code_etat, date_sup=now)
        if code_etat == self.ETAT_DIRECTION_CONCERNEE:
            DemandeConge.objects.filter(id=self.pk).update(etat=code_etat, date_direction=now)
        if code_etat == self.ETAT_DIRECTION_RH:
            DemandeConge.objects.filter(id=self.pk).update(etat=code_etat, date_direction_rh=now)

    def get_notif_receiver(self):
        if self.etat == self.ETAT_ENVOI:
            return self.get_employe().get_superieur_hierarchique()
        if self.etat == self.ETAT_SUPERIEUR_HIERARCHIQUE:
            return self.get_employe().get_departement().get_directeur()
        if self.etat == self.ETAT_DIRECTION_CONCERNEE:
            return Departement.objects.safe_get(id=5).get_directeur()
        if self.etat == self.ETAT_DIRECTION_RH:
            return self.get_employe()
        if self.etat == self.ETAT_REFUS:
            return self.get_employe()

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
        if self.date_sup:
            return self.date_sup
        else:
            return None

    def get_date_direction(self):
        if self.date_direction:
            return self.date_direction
        else:
            return None

    def get_date_direction_rh(self):
        if self.date_direction_rh:
            return self.date_direction_rh
        else:
            return None

    @property
    def in_conge(self):

        date_retour = DemandeConge.objects.filter(employe=self.get_employe(), etat=self.ETAT_DIRECTION_RH)\
            .order_by('-id').first().get_date_retour()
        if date_retour > now().date():
            return True
        else:
            return False



