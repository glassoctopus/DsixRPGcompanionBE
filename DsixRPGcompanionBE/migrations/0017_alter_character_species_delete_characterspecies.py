# Generated by Django 4.1.3 on 2024-12-07 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0016_alter_character_species'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='species',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='DsixRPGcompanionBE.species'),
        ),
        migrations.DeleteModel(
            name='CharacterSpecies',
        ),
    ]