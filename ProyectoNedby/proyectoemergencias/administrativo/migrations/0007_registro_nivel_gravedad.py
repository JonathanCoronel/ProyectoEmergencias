# Generated by Django 5.0.6 on 2024-07-26 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0006_remove_ubicaciondolor_paciente'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='nivel_gravedad',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
