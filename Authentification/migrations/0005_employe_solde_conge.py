# Generated by Django 2.2.3 on 2019-08-02 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentification', '0004_auto_20190802_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='employe',
            name='solde_conge',
            field=models.IntegerField(blank=True, null=True, verbose_name='Solde Jours Possibles Congés'),
        ),
    ]
