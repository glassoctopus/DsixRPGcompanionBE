# Generated by Django 4.1.3 on 2025-01-24 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0024_ability_source'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ability',
            old_name='source',
            new_name='ability_source',
        ),
    ]
