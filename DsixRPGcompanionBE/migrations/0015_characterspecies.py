# Generated by Django 4.1.3 on 2024-12-05 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0014_alter_species_species_average_height_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterSpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_species', to='DsixRPGcompanionBE.character')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='species_characters', to='DsixRPGcompanionBE.species')),
            ],
            options={
                'verbose_name': 'Character Species',
            },
        ),
    ]
