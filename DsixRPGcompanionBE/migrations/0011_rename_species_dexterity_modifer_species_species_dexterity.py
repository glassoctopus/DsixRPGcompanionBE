# Generated by Django 4.1.3 on 2024-10-26 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0010_species_specialability'),
    ]

    operations = [
        migrations.RenameField(
            model_name='species',
            old_name='species_dexterity_modifer',
            new_name='species_dexterity',
        ),
    ]
