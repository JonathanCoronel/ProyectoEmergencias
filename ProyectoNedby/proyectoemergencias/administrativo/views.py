from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from administrativo.models import Paciente, Registro ,UbicacionDolor
from administrativo.forms import PacienteForm, RegistroForm ,UbicacionDolorForm

def index(request):
    registros = Registro.objects.all()

    informacion_template = {'registros': registros, 'numero_usuarios': len(registros)}
    return render(request, 'index.html',informacion_template)

def crear_paciente(request):
    if request.method == 'POST':
        formulario = PacienteForm(request.POST)
        if formulario.is_valid():
            nuevo_paciente = formulario.save()
            return redirect('registro', pk=nuevo_paciente.pk)
    else:
        formulario = PacienteForm()

    contexto = {'formulario': formulario}
    return render(request, 'crearPaciente.html', contexto)

# views.py

from django.shortcuts import render
from .models import Paciente, Registro

def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    pacientes_con_prioridad = []

    for paciente in pacientes:
        ultimo_registro = Registro.objects.filter(paciente=paciente).order_by('-fecha_hora').first()
        if ultimo_registro:
            pacientes_con_prioridad.append((paciente, ultimo_registro.nivel_gravedad))
        else:
            pacientes_con_prioridad.append((paciente, None))

    informacion_template = {
        'pacientes_con_prioridad': pacientes_con_prioridad,
        'numero_pacientes': len(pacientes),
    }

    return render(request, 'listadoPacientes.html', informacion_template)


def registro(request, pk=None):
    formulario_registro = RegistroForm(request.POST or None)
    formulario_paciente = PacienteForm(request.POST or None)

    paciente = None
    if pk:
        paciente = get_object_or_404(Paciente, pk=pk)
        formulario_registro.initial['paciente'] = paciente

    if request.method == 'POST':
        if formulario_registro.is_valid():
            registro = formulario_registro.save(commit=False)
            registro.paciente = paciente
            registro.save()
            return redirect('registro_fisico', registro_id=registro.id)
        elif formulario_paciente.is_valid():
            paciente_nuevo = formulario_paciente.save()
            return redirect('registro', pk=paciente_nuevo.id)

    contexto = {
        'formulario_registro': formulario_registro,
        'formulario_paciente': formulario_paciente,
    }
    return render(request, 'crearRegistro.html', contexto)



def registro_fisico(request, registro_id):
    registro = get_object_or_404(Registro, pk=registro_id)

    if request.method == 'POST':
        tipo_dolor = request.POST.get('pain_type')
        location_x = request.POST.get('location_x')
        location_y = request.POST.get('location_y')

        try:
            location_x = float(location_x)
            location_y = float(location_y)
        except ValueError:
            return HttpResponse("Coordenadas inválidas", status=400)

        # Determinar el área del cuerpo basándose en las coordenadas
        if 10 <= location_y <= 110 and 200 <= location_x <= 300:
            area = 'Cabeza'
        elif 110 < location_y <= 260 and 180 <= location_x <= 320:
            area = 'Torso'
        elif 260 < location_y <= 360 and 180 <= location_x <= 320:
            area = 'Cadera'
        elif 360 < location_y <= 560 and 190 <= location_x <= 310:
            area = 'Piernas'
        else:
            area = 'Fuera del cuerpo'

        if tipo_dolor and location_x and location_y:
            UbicacionDolor.objects.create(
                registro=registro,
                ubicacion=area,  # Guardar área en lugar de coordenadas
                tipo_dolor=tipo_dolor
            )
            return redirect('registros_paciente', paciente_id=registro.paciente.id)

    contexto = {
        'registro': registro,
    }
    return render(request, 'registroFisico.html', contexto)




def registros_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    registros = Registro.objects.filter(paciente=paciente).order_by('-fecha_hora')
    ubicaciones_dolor = UbicacionDolor.objects.filter(registro__paciente=paciente).order_by('registro__fecha_hora')
    

    registros_con_alertas = []
    previous = None

    for registro in registros:
        alertas = {}
        if previous:
            print("-------------------")
            if registro.frecuencia_cardiaca < previous.frecuencia_cardiaca:
                alertas['frecuencia_cardiaca'] = 'Frecuencia Cardiaca Aumentando'
            elif registro.frecuencia_cardiaca > previous.frecuencia_cardiaca:
                alertas['frecuencia_cardiaca'] = 'Frecuencia Cardiaca Disminuyendo'

            if registro.frecuencia_respiratoria < previous.frecuencia_respiratoria:
                alertas['frecuencia_respiratoria'] = 'Frecuencia Respiratoria Aumentando'
            elif registro.frecuencia_respiratoria > previous.frecuencia_respiratoria:
                alertas['frecuencia_respiratoria'] = 'Frecuencia Respiratoria Disminuyendo'

            if registro.presion_arterial_sistolica < previous.presion_arterial_sistolica:
                alertas['presion_arterial_sistolica'] = 'Presión Sistólica Aumentando'
            elif registro.presion_arterial_sistolica > previous.presion_arterial_sistolica:
                alertas['presion_arterial_sistolica'] = 'Presión Sistólica Disminuyendo'

            if registro.presion_arterial_diastolica < previous.presion_arterial_diastolica:
                alertas['presion_arterial_diastolica'] = 'Presión Diastólica Aumentando'
            elif registro.presion_arterial_diastolica > previous.presion_arterial_diastolica:
                alertas['presion_arterial_diastolica'] = 'Presión Diastólica Disminuyendo'

            if registro.saturacion_oxigeno < previous.saturacion_oxigeno:
                alertas['saturacion_oxigeno'] = 'Saturación de Oxígeno Aumentando'
            elif registro.saturacion_oxigeno > previous.saturacion_oxigeno:
                alertas['saturacion_oxigeno'] = 'Saturación de Oxígeno Disminuyendo'

            if registro.temperatura < previous.temperatura:
                alertas['temperatura'] = 'Temperatura Aumentando'
            elif registro.temperatura > previous.temperatura:
                alertas['temperatura'] = 'Temperatura Disminuyendo'

        registros_con_alertas.append((registro, alertas))
        previous = registro

    if request.method == 'POST':
        formulario_registro = RegistroForm(request.POST)
        if formulario_registro.is_valid():
            nuevo_registro = formulario_registro.save(commit=False)
            nuevo_registro.paciente = paciente
            nuevo_registro.save()

            # Limpiar alertas anteriores
            registros_con_alertas.clear()

            # Reconstruir alertas con el nuevo registro
            registros = Registro.objects.filter(paciente=paciente).order_by('-fecha_hora')
            previous = None

            for registro in registros:
                alertas = {}
                if previous:
                    if registro.frecuencia_cardiaca < previous.frecuencia_cardiaca:
                        alertas['frecuencia_cardiaca'] = 'Frecuencia Cardiaca Aumentando'
                    elif registro.frecuencia_cardiaca > previous.frecuencia_cardiaca:
                        alertas['frecuencia_cardiaca'] = 'Frecuencia Cardiaca Disminuyendo'

                    if registro.frecuencia_respiratoria < previous.frecuencia_respiratoria:
                        alertas['frecuencia_respiratoria'] = 'Frecuencia Respiratoria Aumentando'
                    elif registro.frecuencia_respiratoria > previous.frecuencia_respiratoria:
                        alertas['frecuencia_respiratoria'] = 'Frecuencia Respiratoria Disminuyendo'

                    if registro.presion_arterial_sistolica < previous.presion_arterial_sistolica:
                        alertas['presion_arterial_sistolica'] = 'Presión Sistólica Aumentando'
                    elif registro.presion_arterial_sistolica > previous.presion_arterial_sistolica:
                        alertas['presion_arterial_sistolica'] = 'Presión Sistólica Disminuyendo'

                    if registro.presion_arterial_diastolica < previous.presion_arterial_diastolica:
                        alertas['presion_arterial_diastolica'] = 'Presión Diastólica Aumentando'
                    elif registro.presion_arterial_diastolica > previous.presion_arterial_diastolica:
                        alertas['presion_arterial_diastolica'] = 'Presión Diastólica Disminuyendo'

                    if registro.saturacion_oxigeno < previous.saturacion_oxigeno:
                        alertas['saturacion_oxigeno'] = 'Saturación de Oxígeno Aumentando'
                    elif registro.saturacion_oxigeno > previous.saturacion_oxigeno:
                        alertas['saturacion_oxigeno'] = 'Saturación de Oxígeno Disminuyendo'

                    if registro.temperatura < previous.temperatura:
                        alertas['temperatura'] = 'Temperatura Aumentando'
                    elif registro.temperatura > previous.temperatura:
                        alertas['temperatura'] = 'Temperatura Disminuyendo'

                registros_con_alertas.append((registro, alertas))
                previous = registro

    contexto = {
        'paciente': paciente,
        'registros_con_alertas': registros_con_alertas,
        'ubicaciones_dolor': ubicaciones_dolor,
    }
    return render(request, 'registrosPaciente.html', contexto)
