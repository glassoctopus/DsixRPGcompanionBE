# Generated by Django 4.1.3 on 2024-08-23 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charactergroup',
            name='characters',
            field=models.ManyToManyField(blank=True, related_name='chatacter_groups', to='DsixRPGcompanionBE.character'),
        ),
    ]
