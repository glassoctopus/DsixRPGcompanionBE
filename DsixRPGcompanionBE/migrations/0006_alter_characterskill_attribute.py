# Generated by Django 4.1.3 on 2024-09-02 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0005_characterskill_attribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characterskill',
            name='attribute',
            field=models.CharField(default='Error_loading_Attribute', max_length=69),
        ),
    ]