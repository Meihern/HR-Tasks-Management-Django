from django.db import models
from Authentification.models import Employe
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class Notification(models.Model):

    sender = models.ForeignKey(Employe, on_delete=models.CASCADE, verbose_name='Emétteur', null=False, blank=False, related_name='sender')
    receiver = models.ForeignKey(Employe, on_delete=models.CASCADE ,verbose_name='Récepteur', null=False, blank=False, related_name='receiver')
    seen = models.BooleanField(default=False, null=False, blank=False, verbose_name='Vu')
    subject = models.CharField(max_length=50, null=False, blank=False, verbose_name='Sujet')
    message = models.TextField(null=True, blank=True)
    time_sent = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return "Sujet : %s"%(self.subject)

    def get_message(self):
        return self.message

    def get_content_object(self):
        return self.content_object

    @property
    def is_seen(self):
        return self.seen

    def update_seen_status(self):
        Notification.objects.filter(id=self.pk).update(seen=True)

    class Meta:
        verbose_name = 'Notifcation'
        verbose_name_plural = 'Notifications'