from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms

from administrativo.models import Paciente, Registro
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'  # Muestra todos los campos del modelo

        widgets = {
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d'),  # Formato de fecha personalizado
            'genero': forms.Select(choices=[('M', 'Masculino'), ('F', 'Femenino')]),  # Widget de selección para género
        }



class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = '__all__'  # Incluir todos los campos del modelo

        # Opcional: Personalización de campos del formulario
        widgets = {
            'fecha_hora': forms.HiddenInput(),  # Ocultar el campo de fecha y hora (generado automáticamente)
            'paciente': forms.Select(),  # Usar un widget Select para el campo paciente (menú desplegable)
        }
