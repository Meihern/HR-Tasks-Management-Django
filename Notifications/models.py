from django.db import models
from Authentification.models import Employe, Activite, Departement
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from Authentification.manager import CustomModelManager
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
from Fiche_Evaluation.models import FicheObjectif
from Gestion_Attestations.models import DemandeAttestation
from Gestion_Conge.models import DemandeConge


def set_message_attestation():
    return str(DemandeAttestation)


class Notification(models.Model):

    sender = models.ForeignKey(Employe, on_delete=models.CASCADE, verbose_name='Emétteur', null=False, blank=False, related_name='sender')
    receiver = models.ForeignKey(Employe, on_delete=models.CASCADE, verbose_name='Récepteur', null=False, blank=False, related_name='receiver')
    seen = models.BooleanField(default=False, null=False, blank=False, verbose_name='Vu')
    no_reply = models.BooleanField(default=True, null=False, blank=False, verbose_name='Pas de réponse nécessaire')
    subject = models.CharField(max_length=100, null=False, blank=False, verbose_name='Sujet')
    message = models.TextField(null=True, blank=True)
    time_sent = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    objects = CustomModelManager()

    # Méthodes getters

    def __str__(self):  # to_string function
        return "Sujet : %s" % self.subject

    def get_subject(self):
        return self.subject

    def get_message(self):
        return self.message

    def get_receiver(self):
        return self.receiver

    def get_sender(self):
        return self.sender

    def get_content_object(self) -> object:
        return self.content_object

    def get_content_type(self):
        return self.content_type

    # Méthodes setters

    def set_notif_receiver_fiche_objectif(self):
        return self.get_content_object().get_employe().get_superieur_hierarchique()

    def set_notif_receiver_attestation(self):
        activite_mdlz = Activite.objects.safe_get(id=5)
        activite_shared_tabac_fmcg = Activite.objects.safe_get(id=3)
        if self.get_content_object().get_employe().get_activite() == activite_mdlz:
            return Employe.objects.filter(activite=activite_mdlz, consultant_attestations=True).first()
        else:
            return Employe.objects.filter(activite=activite_shared_tabac_fmcg, consultant_attestations=True).first()

    def set_notif_receiver_conge(self):

        if self.get_content_object().get_etat() == self.get_content_object().ETAT_ENVOI:
            return self.get_sender().get_superieur_hierarchique()

        if self.get_content_object().get_etat() == self.get_content_object().ETAT_SUPERIEUR_HIERARCHIQUE: # potentially has to change to get_superieur_hierarchique()
            return self.get_sender().get_superieur_hierarchique()

        if self.get_content_object().get_etat() == self.get_content_object().ETAT_DIRECTION_CONCERNEE:
            return Departement.objects.safe_get(id=5).get_directeur()

        if self.get_content_object().get_etat() == self.get_content_object().ETAT_DIRECTION_RH:
            return self.get_content_object().get_employe()

        if self.get_content_object().get_etat() == self.get_content_object().ETAT_REFUS:
            return self.get_content_object().get_employe()

    def set_subject(self, subject: str):
        self.subject = subject

    def set_message(self, message: str):
        self.message = message

    def set_sender(self, sender: Employe):
        self.sender = sender

    def set_receiver(self):
        if type(self.get_content_object()) == DemandeAttestation:
            self.receiver = self.set_notif_receiver_attestation()
        elif type(self.get_content_object()) == DemandeConge:
            self.receiver = self.set_notif_receiver_conge()
        elif type(self.get_content_object()) == FicheObjectif:
            self.receiver = self.set_notif_receiver_fiche_objectif()
        else:
            return None

    @property
    def is_seen(self):
        return self.seen

    @property
    def is_no_reply(self):
        return self.no_reply

    def update_seen_status(self):
        Notification.objects.filter(id=self.pk).update(seen=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'


