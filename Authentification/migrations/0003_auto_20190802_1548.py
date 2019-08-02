# Generated by Django 2.2.3 on 2019-08-02 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentification', '0002_auto_20190802_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agence',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id_agence')),
                ('nom_agence', models.CharField(max_length=20, verbose_name='Nom Agence')),
            ],
            options={
                'verbose_name': 'Agence',
                'verbose_name_plural': 'Agences',
            },
        ),
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id_cost_center')),
                ('nom_cost_center', models.CharField(max_length=20, verbose_name='Nom Cost Center')),
            ],
            options={
                'verbose_name': 'Cost Center',
                'verbose_name_plural': 'Cost Centers',
            },
        ),
        migrations.AddField(
            model_name='employe',
            name='code_agent',
            field=models.IntegerField(blank=True, null=True, verbose_name='Code agent'),
        ),
        migrations.AddField(
            model_name='employe',
            name='code_edition_comm',
            field=models.IntegerField(blank=True, null=True, verbose_name='Code edition comm.'),
        ),
        migrations.AddField(
            model_name='employe',
            name='commentaire',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employe',
            name='mode_reglement',
            field=models.CharField(blank=True, default='V', max_length=1, null=True, verbose_name='Mode de réglement'),
        ),
        migrations.AddField(
            model_name='employe',
            name='section',
            field=models.IntegerField(blank=True, null=True, verbose_name='Section'),
        ),
        migrations.AddField(
            model_name='employe',
            name='type_base_salariale',
            field=models.CharField(blank=True, default='F', max_length=1, null=True, verbose_name='Type base salariale'),
        ),
        migrations.AddField(
            model_name='employe',
            name='type_cp',
            field=models.IntegerField(blank=True, null=True, verbose_name='Type CP.'),
        ),
        migrations.AddField(
            model_name='employe',
            name='agence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Authentification.Agence', verbose_name='Agence'),
        ),
        migrations.AddField(
            model_name='employe',
            name='cost_center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Authentification.CostCenter', verbose_name='Cost Center'),
        ),
    ]
