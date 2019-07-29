from django.db import models
from Authentification.models import Employe
from django.utils import timezone
# Create your models here.


class Notification(models.Model):

    sender = models.ForeignKey(Employe, on_delete=models.CASCADE, verbose_name='Emétteur', null=False, blank=False, related_name='sender')
    receiver = models.ForeignKey(Employe, on_delete=models.CASCADE ,verbose_name='Récepteur', null=False, blank=False, related_name='receiver')
    seen = models.BooleanField(default=False, null=False, blank=False, verbose_name='Vu')
    subject = models.CharField(max_length=50, null=False, blank=False, verbose_name='Sujet')
    message = models.TextField(null=True, blank=True)
    time_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Sujet : %s"%(self.subject)

    def get_message(self):
        return self.message

    @property
    def is_seen(self):
        return self.seen

    def update_seen_status(self):
        self.seen = True

    class Meta:
        verbose_name = 'Notifcation'
        verbose_name_plural = 'Notifications'