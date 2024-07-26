from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms

from administrativo.models import Paciente, Registro, UbicacionDolor

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'  # Muestra todos los campos del modelo
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'input-fecha-nacimiento', 'placeholder': 'YYYY-MM-DD'}),
            'genero': forms.Select(attrs={'class': 'input-genero'}),
        }

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = '__all__'  # Incluir todos los campos del modelo, incluyendo nivel_gravedad
        labels = {
            'paciente': _('Paciente'),
            'fecha_hora': _('Fecha y Hora'),
            'frecuencia_cardiaca': _('Frecuencia Cardíaca'),
            'frecuencia_respiratoria': _('Frecuencia Respiratoria'),
            'presion_arterial_sistolica': _('Presión Arterial Sistólica'),
            'presion_arterial_diastolica': _('Presión Arterial Diastólica'),
            'saturacion_oxigeno': _('Saturación de Oxígeno'),
            'temperatura': _('Temperatura'),
            'nivel_gravedad': _('Nivel de Gravedad'),  # Nueva etiqueta
        }
        widgets = {
            'fecha_hora': forms.HiddenInput(),
            'paciente': forms.Select(attrs={'class': 'input-paciente'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'input-frecuencia-cardiaca'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'input-frecuencia-respiratoria'}),
            'presion_arterial_sistolica': forms.NumberInput(attrs={'class': 'input-presion-arterial-sistolica'}),
            'presion_arterial_diastolica': forms.NumberInput(attrs={'class': 'input-presion-arterial-diastolica'}),
            'saturacion_oxigeno': forms.NumberInput(attrs={'class': 'input-saturacion-oxigeno'}),
            'temperatura': forms.NumberInput(attrs={'class': 'input-temperatura'}),
            'nivel_gravedad': forms.HiddenInput(),  # Oculto porque se calculará automáticamente
        }


class UbicacionDolorForm(forms.ModelForm):
    class Meta:
        model = UbicacionDolor
        fields = ['ubicacion', 'tipo_dolor']
        labels = {
            'ubicacion': _('Ubicación del Dolor'),
            'tipo_dolor': _('Tipo de Dolor'),
        }
        widgets = {
            'ubicacion': forms.TextInput(attrs={'class': 'input-ubicacion'}),
            'tipo_dolor': forms.TextInput(attrs={'class': 'input-tipo-dolor'}),
        }
