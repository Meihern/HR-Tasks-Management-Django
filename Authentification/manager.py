from django.contrib.auth.models import BaseUserManager



class EmployeManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False, **kwargs):
        employe = None
        if not email:
            if not email:
                raise ValueError("Users must have an email address")
            if not password:
                employe.set_password('azerty258')
        employe = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        employe.set_password(password)  # change user password
        employe.staff = is_staff
        employe.admin = is_admin
        employe.active = is_active
        employe.save(using=self._db)
        return employe

    def create_staffuser(self, email, password=None,**kwargs):
        employe = self.create_user(
            email,
            password=password,
            is_staff=True,
            **kwargs
        )
        employe.save(using=self.db)
        return employe

    def create_superuser(self, email, password=None,**kwargs):
        employe = self.create_user(
            email,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=True,
            **kwargs
        )
        print(employe)
        employe.save(using=self.db)
        return employe
