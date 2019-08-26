from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import EmployeManager, CustomModelManager


# Create your models here.


class Employe(AbstractBaseUser):
    # Choix constants

    SEXE_MASCULIN = 'M'
    SEXE_FEMININ = 'F'
    CHOIX_SEXE = ((SEXE_MASCULIN, 'Masculin'),
                  (SEXE_FEMININ, 'FEMININ'))
    SITUATION_CELIB = 'C'
    SITUATION_MARIE = 'M'
    CHOIX_SITUATION_FAMILLE = ((SITUATION_CELIB, 'Célibataire'),
                               (SITUATION_MARIE, 'Marié'))
    # Attributs

    matricule_paie = models.CharField(primary_key=True, unique=True, max_length=10, verbose_name='Matricule Paie')
    full_name = models.CharField(max_length=60, null=True, blank=True, verbose_name='Nom Prénom')
    fonction = models.CharField(max_length=50, blank=True, null=True, verbose_name='Fonction')
    date_naissance = models.DateField(verbose_name='Date de Naissance', blank=True, null=True)
    sexe = models.CharField(max_length=1, choices=CHOIX_SEXE, verbose_name='Sexe', null=True, blank=True)
    adresse = models.CharField(max_length=255, blank=True, null=True, verbose_name='Adresse')
    ville = models.CharField(max_length=30, blank=True, null=True, verbose_name='Ville')
    n_cin = models.CharField(max_length=10, unique=True, verbose_name='Numéro de Cin', null=True, blank=True)
    nationalite_paie = models.CharField(max_length=3, null=True, blank=True, verbose_name='Nationalité Paie')
    situation_famille = models.CharField(max_length=1, null=True, blank=True, verbose_name='Situation de famille',
                                         choices=CHOIX_SITUATION_FAMILLE)
    date_entree = models.DateField(verbose_name='Date Entrée', blank=True, null=True)
    date_anciennete = models.DateField(verbose_name='Date Ancienneté', blank=True, null=True)
    n_cnss = models.IntegerField(verbose_name='Numéro CNSS', blank=True, null=True, unique=True)
    agence = models.ForeignKey('Agence', on_delete=models.SET_NULL, verbose_name='Agence', null=True, blank=True)
    date_sortie = models.DateField(verbose_name='Date de Sortie', blank=True, null=True)
    superieur_hierarchique = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                               verbose_name='Supérieur Hiérarchique')
    type_contrat = models.CharField(max_length=6, null=True, blank=True, verbose_name='Type de Contrat')
    date_fin_contrat = models.DateField(verbose_name='Date Fin Contrat', null=True, blank=True)
    department = models.ForeignKey('Departement', on_delete=models.SET_NULL, verbose_name='Département', null=True,
                                   blank=True, )
    activite = models.ForeignKey('Activite', on_delete=models.SET_NULL, verbose_name='Activité', null=True,
                                 blank=True)
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, verbose_name='Service', null=True,
                                blank=True)
    cost_center = models.ForeignKey('CostCenter', on_delete=models.SET_NULL, verbose_name='Cost Center', null=True,
                                    blank=True)

    email = models.CharField(max_length=50, verbose_name='Adresse Electronique', unique=False, null=True, blank=False)
    n_compte = models.CharField(max_length=25, null=True, blank=True, unique=True, verbose_name='Numéro de Compte RIB')
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    consultant_attestations = models.BooleanField(default=False)
    consultant_conges = models.BooleanField(default=False)
    consultant_recrutements = models.BooleanField(default=False)
    consultant_fiches_objectifs = models.BooleanField(default=False)

    # Django User Model Settings
    USERNAME_FIELD = 'matricule_paie'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'
    objects = EmployeManager()

    # Méthodes

    def __str__(self):
        if self.full_name:
            return self.full_name
        elif self.email:
            return self.email
        else:
            return self.matricule_paie

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        if self.full_name:
            return self.full_name
        elif self.email:
            return self.email
        else:
            return self.matricule_paie

    def get_last_login(self):
        return self.last_login

    def get_matricule(self):
        return self.matricule_paie

    def get_email(self):
        if self.email:
            return self.email
        else:
            return None

    def get_sexe_nomination(self):
        if self.sexe == 'F':
            return 'Mme'
        elif self.sexe == 'M':
            return 'Mr'
        else:
            return 'M.'

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

    def get_activite(self):
        return self.activite

    def get_departement(self):
        return self.department

    def get_username(self):
        return self.matricule_paie

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_solde_conge(self):
        if self.solde_conge is None:
            return 0
        else:
            return self.solde_conge

    def is_superieur_to(self, employe):
        if employe.get_superieur_hierarchique() == self:
            return True
        else:
            return False

    # Properties

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    @property
    def can_consult_attestations(self):
        return self.consultant_attestations

    @property
    def can_consult_conges(self):
        return self.consultant_conges

    @property
    def can_consult_recrutements(self):
        return self.consultant_recrutements

    @property
    def can_consult_fiches_objectifs(self):
        return self.consultant_fiches_objectifs

    @property
    def can_consult_mdlz(self):
        activite_mdlz = Activite.objects.safe_get(id=5)
        if self.activite == activite_mdlz:
            return True
        else:
            return False

    @property
    def can_consult_shared_tabac_fmcg(self):
        activite_shared_tabac_fmcg = Activite.objects.safe_get(id=3)
        if self.activite == activite_shared_tabac_fmcg:
            return True
        else:
            return False

    @property
    def can_consult_shared(self):
        activite_shared = Activite.objects.safe_get(id=4)
        if self.activite == activite_shared:
            return True
        else:
            return False

    @property
    def is_consultant(self):
        if self.can_consult_conges or self.can_consult_attestations or self.can_consult_recrutements:
            return True
        else:
            return False

    class Meta:
        verbose_name = 'Employé'
        verbose_name_plural = 'Employés'


class Departement(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='id_Département')
    nom_departement = models.CharField(max_length=50, unique=True, null=False, blank=False,
                                       verbose_name='Nom Département')
    directeur = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomModelManager()

    def __str__(self):
        return self.nom_departement

    def get_directeur(self):
        return self.directeur

    class Meta:
        verbose_name = 'Département'
        verbose_name_plural = 'Départements'


class Activite(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='id_Activité')
    nom_activite = models.CharField(max_length=20, verbose_name='Nom Activité', null=False, blank=False)

    objects = CustomModelManager()

    def __str__(self):
        return self.nom_activite

    class Meta:
        verbose_name = 'Activité'
        verbose_name_plural = 'Activités'


class Service(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='id_Service')
    nom_service = models.CharField(max_length=50, verbose_name='Nom Service', null=False, blank=False)

    objects = CustomModelManager()

    def __str__(self):
        return self.nom_service

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Agence(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='id_agence')
    nom_agence = models.CharField(max_length=20, verbose_name='Nom Agence', null=False, blank=False)

    objects = CustomModelManager()

    def __str__(self):
        return self.nom_agence

    class Meta:
        verbose_name = 'Agence'
        verbose_name_plural = 'Agences'


class CostCenter(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='id_cost_center')
    nom_cost_center = models.CharField(max_length=20, verbose_name='Nom Cost Center', null=False, blank=False)

    objects = CustomModelManager()

    def __str__(self):
        return self.nom_cost_center

    class Meta:
        verbose_name = 'Cost Center'
        verbose_name_plural = 'Cost Centers'
