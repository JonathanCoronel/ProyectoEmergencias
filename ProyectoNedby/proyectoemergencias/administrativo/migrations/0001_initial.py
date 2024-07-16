# Generated by Django 5.0.6 on 2024-07-16 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('cedula', models.CharField(max_length=30, unique=True)),
                ('fecha_nacimiento', models.DateField()),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.IntegerField()),
            ],
        ),
    ]
