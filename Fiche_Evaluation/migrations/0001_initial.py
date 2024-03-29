# Generated by Django 2.2.3 on 2019-09-02 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessibiliteFicheObjectif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mois_accessibilite_remplir_fiche', models.IntegerField(blank=True, choices=[(1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')], null=True, verbose_name="Mois d'accessibilité pour remplir les fiches d'objectifs")),
                ('mois_accessibilite_evaluation_mi_annuelle', models.IntegerField(blank=True, choices=[(1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')], null=True, verbose_name="Mois d'accessibilité pour évaluation mi-annuelle des  fiches d'objectifs")),
                ('mois_accessibilite_evaluation_annuelle', models.IntegerField(blank=True, choices=[(1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')], null=True, verbose_name="Mois d'accessibilité pour évaluation Annuelle des  fiches d'objectifs")),
                ('remplir_exceptionnelle_is_accessible', models.BooleanField(default=False, verbose_name="Etat exceptionnel d'accessibilité pour remplir les fiche des objectifs")),
                ('evaluation_mi_annee_exceptionnelle_is_accessible', models.BooleanField(default=False, verbose_name="Etat exceptionnel d'accessibilité pour evaluation mi-annuelle des fiche d'objectifs")),
                ('evaluation_annee_exceptionnelle_is_accessible', models.BooleanField(default=False, verbose_name="Etat exceptionnel d'accessibilité pour evaluation annuelle des fiche d'objectifs")),
            ],
            options={
                'verbose_name': "Permission d'accesibilité aux fonctionnalités Fiche Objectif",
                'verbose_name_plural': "Permissions d'accesibilité aux fonctionnalités Fiche Objectif",
            },
        ),
        migrations.CreateModel(
            name='FicheObjectif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_envoi', models.DateField(default=django.utils.timezone.now)),
                ('bonus', models.FloatField(blank=True, null=True, verbose_name='Bonus')),
                ('valide', models.BooleanField(default=False)),
                ('commentaire_manager', models.TextField(blank=True, null=True, verbose_name='Commentaire du Manager Performance Annuelle')),
                ('commentaire_employe', models.TextField(blank=True, null=True, verbose_name='Commentaire Employé Performance Annuelle')),
                ('date_validation_manager', models.DateField(blank=True, null=True, verbose_name='Date Validation Manager Annuelle')),
                ('date_validation_employe', models.DateField(blank=True, null=True, verbose_name='Date Validation Employé Annuelle')),
                ('employe', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL, verbose_name='Employé')),
            ],
            options={
                'verbose_name': 'Fiche des objectifs',
                'verbose_name_plural': 'Les fiches des objectifs',
            },
        ),
        migrations.CreateModel(
            name='Objectif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('poids', models.FloatField(verbose_name='Poids')),
                ('notation_manager', models.FloatField(blank=True, choices=[(1.25, 'HP+'), (1.2, 'HP='), (1.15, 'HP-'), (1.1, 'EP+'), (1.05, 'EP='), (1.03, 'EP-'), (1, 'BP+'), (0.95, 'BP='), (0.85, 'BP-'), (0.75, 'MP+'), (0.5, 'MP'), (0, 'FP')], null=True, verbose_name='Notation Manager')),
                ('evaluation_mi_annuelle', models.TextField(blank=True, null=True, verbose_name='Evalutation Mi-Annuelle')),
                ('evaluation_annuelle', models.TextField(blank=True, null=True, verbose_name='Evalutation Annuelle')),
                ('fiche_objectif', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Fiche_Evaluation.FicheObjectif', verbose_name="Fiche d'objectif associée")),
            ],
            options={
                'verbose_name': 'Objectif',
                'verbose_name_plural': 'Objectifs',
            },
        ),
        migrations.CreateModel(
            name='SousObjectif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('objectif', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Fiche_Evaluation.Objectif', verbose_name='Objectif_Associé')),
            ],
            options={
                'verbose_name': 'Sous Objectif',
                'verbose_name_plural': 'Sous Objectifs',
            },
        ),
    ]
