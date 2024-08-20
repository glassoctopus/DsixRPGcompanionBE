# Generated by Django 4.1.3 on 2024-08-18 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0010_rename_archetype_dexiterity_archetype_archetype_dexterity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='dark_side_points',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='dexterity',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_alter',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_control',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_points',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_sense',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_strength',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='knowledge',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='mechanical',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='perception',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='strength',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='character',
            name='technical',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]