# Generated by Django 4.1.3 on 2025-01-25 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0026_skill_species_skill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='species',
            name='species_ability',
        ),
        migrations.RemoveField(
            model_name='species',
            name='species_skill',
        ),
        migrations.AddField(
            model_name='species',
            name='species_ability',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='species_abilities', to='DsixRPGcompanionBE.ability'),
        ),
        migrations.AddField(
            model_name='species',
            name='species_skill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='species_skills', to='DsixRPGcompanionBE.skill'),
        ),
    ]
