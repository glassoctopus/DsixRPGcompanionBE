# Generated by Django 4.1.3 on 2024-08-24 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0002_alter_charactergroup_characters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='a_quote',
            field=models.CharField(blank=True, max_length=1369, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='age',
            field=models.IntegerField(blank=True, default=21, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='background',
            field=models.CharField(blank=True, max_length=1369, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='credits',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='dark_side_points',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='dexterity',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_alter',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_control',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_points',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_sense',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_sensitive',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='force_strength',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='gender',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='height',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='homeworld',
            field=models.CharField(blank=True, max_length=69, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='image',
            field=models.CharField(blank=True, max_length=223, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='knowledge',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='mechanical',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(blank=True, max_length=69, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='objectives',
            field=models.CharField(blank=True, max_length=1369, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='perception',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='personality',
            field=models.CharField(blank=True, max_length=1369, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='physical_description',
            field=models.CharField(blank=True, max_length=1369, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='species',
            field=models.CharField(blank=True, max_length=69, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='strength',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='technical',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='weight',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
