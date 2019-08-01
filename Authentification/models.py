from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from .manager import EmployeManager


# Create your models here.


class Employe(AbstractBaseUser):
    # Choix constants

    SEXE_MASCULIN = 'M'
    SEXE_FEMININ = 'F'
    CHOIX_SEXE = ((SEXE_MASCULIN, 'Masculin'),
                  (SEXE_FEMININ, 'FEMININ'))
    SITUATION_CELIB = 'C'
    SITUATION_MARIE = 'M'
    CHOIX_SITUATION_FAMILLE = ((SITUATION_CELIB, 'Celibataire'),
                               (SITUATION_MARIE, 'Marie'))
    # Attributs

    matricule_paie = models.CharField(primary_key=True, unique=True, max_length=10, verbose_name='Matricule Paie')
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Nom')
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Prénom')
    fonction = models.CharField(max_length=50, blank=True, null=True, verbose_name='Fonction')
    date_naissance = models.DateField(verbose_name='Date de Naissance', blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=CHOIX_SEXE, verbose_name='Sexe', null=True, blank=True)
    adresse = models.CharField(max_length=255, blank=True, null=True, verbose_name='Adresse')
    ville = models.CharField(max_length=30, blank=True, null=True, verbose_name='Ville')
    n_cin = models.CharField(max_length=10, unique=True, verbose_name='Numero Cin', null=True, blank=True)
    nationalite_paie = models.CharField(max_length=3, null=True, blank=True, verbose_name='Nationalité Paie')
    situation_famille = models.CharField(max_length=1, null=True, blank=True, verbose_name='Situation de famille',
                                         choices=CHOIX_SITUATION_FAMILLE)
    date_entree = models.DateField(verbose_name='Date Entrée', blank=True, null=True)
    date_anciennete = models.DateField(verbose_name='Date Anciennete', blank=True, null=True)
    n_cnss = models.IntegerField(verbose_name='Numéro CNSS', blank=True, null=True)
    date_sortie = models.DateField(verbose_name='Date de Sortie', blank=True, null=True)
    superieur_hierarchique = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                               verbose_name='Supérieur Hierarchique')
    type_contrat = models.CharField(max_length=6, null=True, blank=True, verbose_name='Type de Contrat')
    date_fin_contrat = models.DateField(verbose_name='Date Fin Contrat', null=True, blank=True)
    department = models.ForeignKey('Departement', on_delete=models.SET_NULL, verbose_name='Département', null=True,
                                   blank=True, )
    email = models.CharField(max_length=50, verbose_name='Adresse Electronique', unique=True)
    n_compte = models.CharField(max_length=25, null=False, unique=True, verbose_name='Numéro de Compte RIB')
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    # Django User Model Settings
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['n_cin', 'matricule_paie']
    EMAIL_FIELD = 'email'
    objects = EmployeManager()

    # Méthodes

    def __str__(self):
        if self.last_name and self.first_name:
            return self.last_name + ' ' + self.first_name
        else:
            return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name

    def get_short_name(self):
        if self.last_name:
            return self.last_name
        else:
            return self.email

    def get_last_login(self):
        return self.last_login

    def get_matricule(self):
        return self.matricule_paie

    def get_superieur_hierarchique(self):
        if self.superieur_hierarchique:
            return self.superieur_hierarchique
        else:
            return None

    def get_date_entree(self):
        return self.date_entree

    def get_n_cin(self):
        return self.n_cin

    def get_n_cnss(self):
        return self.n_cnss

    def get_n_compte(self):
        return self.n_compte

    def get_fonction(self):
        return self.fonction

    def get_username(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        verbose_name = 'Employé'
        verbose_name_plural = 'Employés'


class Departement(models.Model):
    nom_departement = models.CharField(max_length=30, unique=True, null=False, blank=False, verbose_name='Departement')
    directeur = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=False)
    nbr_employes = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nom_departement

    def get_directeur(self):
        return self.directeur

    def get_nbr_employes(self):
        return self.nbr_employes

    class Meta:
        verbose_name = 'Département'
        verbose_name_plural = 'Départements'


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


