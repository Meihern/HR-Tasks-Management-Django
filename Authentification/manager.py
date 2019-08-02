from django.contrib.auth.models import BaseUserManager


class EmployeManager(BaseUserManager):

    def create_user(self, matricule_paie, password=None, is_active=True, is_staff=False, is_admin=False, **kwargs):
        employe = None
        if not matricule_paie:
            if not matricule_paie:
                raise ValueError("Le matricule est nécessaire")
            if not password:
                password = 'azerty258'
        employe = self.model(
            email=matricule_paie,
            **kwargs
        )
        print(password)
        employe.set_password(password)  # change user password
        employe.staff = is_staff
        employe.admin = is_admin
        employe.active = is_active
        employe.save(using=self._db)
        return employe

    def create_staffuser(self, matricule_paie, password=None,**kwargs):
        employe = self.create_user(
            matricule_paie,
            password=password,
            is_staff=True,
            **kwargs
        )
        employe.save(using=self.db)
        return employe

    def create_superuser(self, matricule_paie, password=None,**kwargs):
        employe = self.create_user(
            matricule_paie,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=True,
            **kwargs
        )
        print(employe)
        employe.save(using=self.db)
        return employe
