from django.db import models
from Authentification.models import Employe
from django.utils.timezone import now
from Notifications.models import Notification
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.


class TypeDemandeAttestatation(models.Model):
    TYPE_TRAVAIL = 'travail'
    TYPE_SALAIRE = 'salaire'
    TYPE_DOMICILIATION = 'domiciliation'
    CHOIX_TYPES = (
        (TYPE_TRAVAIL, 'Attestation Travail'), (TYPE_SALAIRE, 'Attestation Salaire'),
        (TYPE_DOMICILIATION, 'Domiciliation')
    )
    nom_type_demande = models.CharField(unique=True, max_length=15, verbose_name="Type de la demande d'attestation", blank=False, null=False,
                                        choices=CHOIX_TYPES)

    def __str__(self):
        if self.nom_type_demande == 'domiciliation':
            return "Demande de %s"%(self.nom_type_demande)
        else:
            return "Demande d'attestation de %s"%(self.nom_type_demande)

    class Meta:
        verbose_name = "Type d'attestation"
        verbose_name_plural = "Type des attestations"


class DemandeAttestation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=None, null=False, blank=False, verbose_name="Employe")
    date_envoi = models.DateTimeField(default=now, verbose_name="Date Envoyée", null=False, blank=False)
    etat_validation = models.BooleanField(default=False, null=False, blank=False, verbose_name="Etat de Validation")
    date_validation = models.DateField(null=True, blank=True, verbose_name="Date de Validation")
    type = models.ForeignKey(TypeDemandeAttestatation, on_delete=None, null=False, verbose_name="Type de demande",
                             blank=False)
    notifications = GenericRelation(Notification)

    def update_etat_validation(self):
        DemandeAttestation.objects.filter(id=self.pk).update(etat_validation=True, date_validation=now())

    def get_type_demande(self):
        return self.type

    def get_employe(self):
        return self.employe

    def get_date_validation(self):
        return self.date_validation

    def __str__(self):
        return "%s envoyé par %s" % (self.get_type_demande(), self.employe.get_full_name())

    @property
    def is_valid(self):
        return self.etat_validation

    class Meta:
        verbose_name = "Demande Attestation"
        verbose_name_plural = "Demandes des Attestations"

class Salaire(models.Model):

    matricule_paie = models.OneToOneField(Employe, primary_key=True, on_delete=models.CASCADE, null=False, blank=False,
                                verbose_name='Employé', db_column='matricule_paie')
    valeur_brute = models.IntegerField(null=False, blank=False, verbose_name='Salaire Brute')

    def __str__(self):
        return ('%s')%self.valeur_brute

    def get_valeur_brute(self):
        return self.valeur_brute

    def get_employe(self):
        return self.matricule_paie

    class Meta:
        verbose_name = 'Salaire'
        verbose_name_plural = 'Salaires'
