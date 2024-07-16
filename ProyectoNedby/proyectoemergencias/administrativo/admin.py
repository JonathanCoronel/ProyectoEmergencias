from django.contrib import admin
from .models import Paciente ,Registro

# Register your models here.

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula','fecha_nacimiento','genero','correo','telefono')
    search_fields = ('nombre', 'apellido', 'cedula','fecha_nacimiento','genero','correo','telefono')

admin.site.register(Paciente, PacienteAdmin)

class RegistroAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_hora', 'frecuencia_cardiaca','frecuencia_respiratoria','presion_arterial_sistolica',
                    'presion_arterial_diastolica','saturacion_oxigeno','temperatura')
    search_fields = ('paciente', 'fecha_hora', 'frecuencia_cardiaca','frecuencia_respiratoria','presion_arterial_sistolica',
                    'presion_arterial_diastolica','saturacion_oxigeno','temperatura')
    raw_id_fields = ('paciente',)

admin.site.register(Registro, RegistroAdmin)

