from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class EmployeManager(BaseUserManager):

    def create_user(self, matricule_paie, password='azerty258', is_active=True, is_staff=False, is_admin=False,
                    can_consult_attestations=False, can_consult_conges=False, can_consult_recrutements=False,**kwargs):

        if not matricule_paie:
            raise ValueError("Le matricule est nécessaire")
        if not password:
            password = 'azerty258'

        employe = self.model(
            matricule_paie=matricule_paie,
            **kwargs
        )
        employe.set_password(password)  # change user password
        employe.staff = is_staff
        employe.admin = is_admin
        employe.active = is_active
        employe.consultant_recrutments = can_consult_recrutements
        employe.consultant_attestations = can_consult_attestations
        employe.consultant_conges = can_consult_conges
        employe.save(using=self._db)
        return employe

    def create_staffuser(self, matricule_paie, password=None, **kwargs):
        employe = self.create_user(
            matricule_paie=matricule_paie,
            password=password,
            is_staff=True,
            **kwargs
        )
        employe.save(using=self.db)
        return employe

    def create_superuser(self, matricule_paie, password=None, **kwargs):
        employe = self.create_user(
            matricule_paie=matricule_paie,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=True,
            **kwargs
        )
        employe.save(using=self.db)
        return employe

    def safe_get(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class CustomModelManager(models.Manager):

    def safe_get(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


