# Generated by Django 4.1.3 on 2024-09-02 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0006_alter_characterskill_attribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characterskill',
            name='attribute',
            field=models.CharField(max_length=69),
        ),
    ]