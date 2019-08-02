# Generated by Django 2.2.3 on 2019-08-02 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentification', '0006_auto_20190802_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activite',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id_Activité')),
                ('nom_activite', models.CharField(max_length=20, verbose_name='Nom_Activité')),
            ],
            options={
                'verbose_name': 'Activité',
                'verbose_name_plural': 'Activités',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id_Service')),
                ('nom_service', models.CharField(max_length=20, verbose_name='Nom_Service')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.AlterField(
            model_name='departement',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='id_Département'),
        ),
        migrations.AddField(
            model_name='employe',
            name='activite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Authentification.Activite', verbose_name='Activité'),
        ),
        migrations.AddField(
            model_name='employe',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Authentification.Service', verbose_name='Service'),
        ),
    ]
