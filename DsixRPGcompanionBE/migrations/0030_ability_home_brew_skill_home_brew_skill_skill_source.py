# Generated by Django 4.1.3 on 2025-02-27 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0029_rename_species_skill_skill_species_specific_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ability',
            name='home_brew',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='skill',
            name='home_brew',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='skill',
            name='skill_source',
            field=models.CharField(blank=True, max_length=1369, null=True),
        ),
    ]
