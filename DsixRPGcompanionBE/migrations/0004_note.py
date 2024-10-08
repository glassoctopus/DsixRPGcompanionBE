# Generated by Django 4.1.3 on 2024-08-25 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DsixRPGcompanionBE', '0003_alter_character_a_quote_alter_character_age_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('temporary_field', models.BooleanField(default=True)),
            ],
        ),
    ]
