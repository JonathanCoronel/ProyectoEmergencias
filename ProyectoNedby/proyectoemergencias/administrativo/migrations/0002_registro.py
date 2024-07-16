# Generated by Django 5.0.6 on 2024-07-16 05:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(auto_now=True)),
                ('frecuencia_cardiaca', models.IntegerField()),
                ('frecuencia_respiratoria', models.IntegerField()),
                ('presion_arterial_sistolica', models.IntegerField()),
                ('presion_arterial_diastolica', models.IntegerField()),
                ('saturacion_oxigeno', models.IntegerField()),
                ('temperatura', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrativo.paciente')),
            ],
        ),
    ]