# Generated by Django 2.2.3 on 2019-08-16 14:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Fiche_Evaluation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficheobjectif',
            name='date_envoi',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]